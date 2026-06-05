import asyncio
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_PLIST_LABEL = "com.aura.bot"
_PLIST_DEST = Path.home() / "Library" / "LaunchAgents" / f"{_PLIST_LABEL}.plist"


def _build_plist_content() -> str:
    """Generate LaunchAgent plist with the actual Python interpreter and project root."""
    python = sys.executable
    project_root = str(_PROJECT_ROOT)
    logs_dir = str(_PROJECT_ROOT / "logs")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{_PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python}</string>
        <string>-m</string>
        <string>src.main</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{project_root}</string>
    <key>StandardOutPath</key>
    <string>{logs_dir}/bot.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{logs_dir}/bot.stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>{Path(python).parent}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>HOME</key>
        <string>{Path.home()}</string>
    </dict>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
"""


class LaunchAgent:
    """Manages bot process lifecycle with keepalive via LaunchAgent plist."""

    def __init__(self) -> None:
        self.process: Optional[asyncio.subprocess.Process] = None
        self.throttle_interval = 10

    async def start(self) -> None:
        """Start the bot process using the current Python interpreter."""
        try:
            self.process = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "src.main",
                cwd=str(_PROJECT_ROOT),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info("Bot process started (PID: %s)", self.process.pid)
        except Exception as e:
            logger.error("Failed to start bot process: %s", e)
            raise

    def stop(self) -> None:
        """Stop the bot process."""
        if self.process and not self.process.returncode:
            self.process.terminate()
            logger.info("Bot process terminated")

    async def restart_loop(self) -> None:
        """Continuously monitor and restart bot if it exits."""
        while True:
            try:
                await self.start()
                await self.process.wait()
                logger.warning(
                    "Bot process exited with code %s, restarting in %ds",
                    self.process.returncode,
                    self.throttle_interval,
                )
                await asyncio.sleep(self.throttle_interval)
            except Exception as e:
                logger.exception("Exception in restart loop: %s", e)
                await asyncio.sleep(self.throttle_interval)


def ensure_launch_agent_is_running() -> bool:
    """Install/refresh the LaunchAgent plist with current paths and (re)load it.

    Generates the plist dynamically so it always reflects the actual Python
    interpreter and project root — even after venv recreation or directory moves.

    Returns:
        True if the LaunchAgent was successfully installed and loaded.
    """
    try:
        # Ensure logs directory exists
        logs_dir = _PROJECT_ROOT / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Write freshly-generated plist
        _PLIST_DEST.parent.mkdir(parents=True, exist_ok=True)
        _PLIST_DEST.write_text(_build_plist_content())
        logger.info("LaunchAgent plist written to %s", _PLIST_DEST)

        # Unload first (ignore errors — may not be loaded yet)
        subprocess.run(
            ["launchctl", "unload", str(_PLIST_DEST)],
            check=False,
            capture_output=True,
        )

        # Load the updated plist
        result = subprocess.run(
            ["launchctl", "load", str(_PLIST_DEST)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            logger.info("LaunchAgent loaded: %s", _PLIST_LABEL)
        else:
            logger.warning(
                "launchctl load returned %s: %s",
                result.returncode,
                result.stderr.strip(),
            )
        return True
    except Exception as e:
        logger.error("Failed to install LaunchAgent: %s", e)
        return False
