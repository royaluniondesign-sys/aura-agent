"""Mesh Loop — AURA↔Hermes autonomous conversation loop.

Runs every 30 minutes. Checks shared tasks for Hermes work, delegates,
and broadcasts the exchange to the owner so they can see what they're doing.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Optional

import structlog

logger = structlog.get_logger()

_INTERVAL_S = 1800  # 30 min between autonomous checks
_TASKS_FILE = Path.home() / ".aura" / "memory" / "shared" / "tasks.md"
_DELEGATED = Path.home() / ".aura" / "mesh" / "delegated.json"
_OPENCLAW_BIN = "/opt/homebrew/bin/openclaw"

# A task not confirmed by Hermes is retried after 24h, up to 3 times total.
_DELEGATED_TTL_S = 86400  # 24h before a stale delegation is retried
_DELEGATED_MAX_ATT = 3  # give up after this many timeout/failure attempts

_loop_status: dict = {
    "running": False,
    "last_run_at": None,
    "last_delegated": None,
    "total_delegations": 0,
}


def get_mesh_loop_status() -> dict:
    return {**_loop_status}


def _load_delegated() -> dict[str, dict]:
    """Load delegated map: {task_text: {ts: float, attempts: int, last_reply: str}}.

    Backwards-compatible: old format was a JSON list of strings.
    """
    if _DELEGATED.exists():
        try:
            data = json.loads(_DELEGATED.read_text())
            if isinstance(data, list):
                # Migrate old list format to new dict format
                return {t: {"ts": 0.0, "attempts": 1, "last_reply": ""} for t in data}
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {}


def _save_delegated(delegated: dict[str, dict]) -> None:
    _DELEGATED.parent.mkdir(parents=True, exist_ok=True)
    _DELEGATED.write_text(json.dumps(delegated, ensure_ascii=False, indent=2))


def _extract_hermes_tasks() -> list[str]:
    """Parse ## Pendientes Hermes section from shared tasks.md."""
    if not _TASKS_FILE.exists():
        return []
    try:
        text = _TASKS_FILE.read_text()
        in_section = False
        tasks = []
        for line in text.splitlines():
            if "## Pendientes Hermes" in line:
                in_section = True
                continue
            if in_section:
                if line.startswith("## "):
                    break
                stripped = line.strip()
                if stripped.startswith("- [ ]"):
                    tasks.append(stripped[5:].strip())
        return tasks
    except Exception:
        return []


async def _call_hermes(task: str, timeout: int = 90) -> tuple[str, float]:
    """Call Hermes and return (reply_text, elapsed_seconds)."""
    import ast

    start = time.time()
    proc = await asyncio.create_subprocess_exec(
        _OPENCLAW_BIN,
        "agent",
        "--agent",
        "main",
        "--message",
        task,
        "--json",
        "--timeout",
        str(timeout),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout + 10)
        raw = stdout.decode("utf-8", errors="replace").strip()
        elapsed = time.time() - start

        data = None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            try:
                result = ast.literal_eval(raw)
                if isinstance(result, dict):
                    data = result
            except Exception:
                pass

        if data:
            payloads = data.get("result", {}).get("payloads", [])
            texts = [
                p.get("text", "")
                for p in payloads
                if isinstance(p, dict) and p.get("text")
            ]
            reply = "\n".join(texts).strip() if texts else raw[:500]
        else:
            reply = raw[:500] if raw else "(sin respuesta)"

        return reply, elapsed

    except asyncio.TimeoutError:
        return f"timeout ({timeout}s)", time.time() - start


async def _run_mesh_check(notify_fn: Optional[Callable] = None) -> None:
    """One autonomous mesh check: delegate pending Hermes tasks."""

    _loop_status["running"] = True
    _loop_status["last_run_at"] = datetime.now(UTC).isoformat()

    try:
        tasks = _extract_hermes_tasks()
        delegated = _load_delegated()
        now = time.time()

        # A task is eligible when: never delegated, OR stale (TTL expired) AND under max attempts
        def _is_eligible(t: str) -> bool:
            if t not in delegated:
                return True
            rec = delegated[t]
            stale = now - rec.get("ts", 0) > _DELEGATED_TTL_S
            under_limit = rec.get("attempts", 0) < _DELEGATED_MAX_ATT
            return stale and under_limit

        new_tasks = [t for t in tasks if _is_eligible(t)]
        if not new_tasks:
            logger.debug("mesh_loop_no_new_tasks")
            return

        # Delegate the first eligible task (one per cycle to avoid spam)
        task = new_tasks[0]
        prior = delegated.get(task, {})
        attempt_num = prior.get("attempts", 0) + 1
        logger.info("mesh_loop_delegating", task=task[:60], attempt=attempt_num)

        message = (
            f"AURA aquí. Tarea pendiente para ti del shared/tasks.md:\n\n"
            f'"{task}"\n\n'
            f"¿Puedes confirmar que la tomaste y qué harás?"
        )

        reply, elapsed = await _call_hermes(message, timeout=90)

        is_timeout = reply.startswith("timeout (") or "timeout" in reply.lower()
        is_error = reply == "(sin respuesta)" or not reply.strip()

        # Log to mesh-log
        _ml = Path.home() / ".aura" / "memory" / "mesh-log.md"
        try:
            _ml.parent.mkdir(parents=True, exist_ok=True)
            _ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
            status_tag = "TIMEOUT" if is_timeout else ("ERROR" if is_error else "OK")
            with open(_ml, "a") as _f:
                _f.write(
                    f"\n[{_ts}] AUTO AURA→HERMES (att {attempt_num}/{_DELEGATED_MAX_ATT})"
                    f" [{status_tag}]: {task[:60]} | reply: {reply[:120]}\n"
                )
        except Exception:
            pass

        # Update delegation record regardless of outcome (tracks attempts)
        delegated[task] = {
            "ts": now,
            "attempts": attempt_num,
            "last_reply": reply[:200],
        }
        _save_delegated(delegated)

        _loop_status["last_delegated"] = task
        _loop_status["total_delegations"] = _loop_status.get("total_delegations", 0) + 1

        if is_timeout or is_error:
            logger.warning(
                "mesh_loop_hermes_no_response",
                task=task[:60],
                attempt=attempt_num,
                reply=reply[:80],
            )
            # Notify owner when Hermes fails to respond — they need to know
            if notify_fn and attempt_num >= _DELEGATED_MAX_ATT:
                try:
                    await notify_fn(
                        f"⚠️ Hermes no respondió a esta tarea {_DELEGATED_MAX_ATT}× seguidas:\n"
                        f"_{task[:100]}_\n"
                        f"Última respuesta: `{reply[:80]}`\n"
                        f"Revisa que openclaw esté funcionando."
                    )
                except Exception:
                    pass
            elif notify_fn and (is_timeout or is_error):
                try:
                    await notify_fn(
                        f"⏱ Hermes timeout (intento {attempt_num}/{_DELEGATED_MAX_ATT}):\n"
                        f"_{task[:80]}_"
                    )
                except Exception:
                    pass
        else:
            logger.info(
                "mesh_loop_delegated_ok", task=task[:60], elapsed_s=round(elapsed, 1)
            )

    except Exception as e:
        logger.warning("mesh_loop_error", error=str(e))
    finally:
        _loop_status["running"] = False


async def _drain_inbox() -> None:
    """Forward any queued Hermes→AURA messages that arrived while bot was offline."""
    from src.infra.mesh_broadcaster import broadcast_alert

    inbox = Path.home() / ".aura" / "mesh" / "inbox.json"
    if not inbox.exists():
        return
    try:
        items = json.loads(inbox.read_text())
        if not items:
            return
        for item in items:
            await broadcast_alert(
                from_agent=item.get("from", "hermes"),
                message=item.get("message", ""),
            )
        inbox.write_text("[]")
        logger.info("mesh_inbox_drained", count=len(items))
    except Exception as e:
        logger.warning("mesh_inbox_drain_error", error=str(e))


async def start_mesh_loop(notify_fn: Optional[Callable] = None) -> None:
    """Long-running loop: drains inbox on start, then checks every 30min."""
    logger.info("mesh_loop_started", interval_min=_INTERVAL_S // 60)

    # Drain any queued messages first
    await asyncio.sleep(15)  # let bot fully start
    await _drain_inbox()

    while True:
        await asyncio.sleep(_INTERVAL_S)
        await _run_mesh_check(notify_fn=notify_fn)
        await _drain_inbox()
