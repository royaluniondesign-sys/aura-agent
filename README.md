<p align="center">
  <img src="https://img.shields.io/badge/AURA-v0.11.1-d97757?style=for-the-badge&labelColor=0e0d0c" alt="AURA v0.11.1">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776ab?style=for-the-badge&labelColor=0e0d0c" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Tests-498_passing-22c55e?style=for-the-badge&labelColor=0e0d0c" alt="498 passing">
  <img src="https://img.shields.io/badge/Brains-11_cascade-7c5cff?style=for-the-badge&labelColor=0e0d0c" alt="11 brains">
  <img src="https://img.shields.io/badge/RAG-11k%2B_chunks-f59e0b?style=for-the-badge&labelColor=0e0d0c" alt="11k+ chunks">
  <img src="https://img.shields.io/badge/License-MIT-475569?style=for-the-badge&labelColor=0e0d0c" alt="MIT">
  <img src="https://github.com/royaluniondesign-sys/aura-agent/actions/workflows/ci.yml/badge.svg" alt="CI">
</p>

<br>

```
█████╗ ██╗   ██╗██████╗  █████╗
██╔══██╗██║   ██║██╔══██╗██╔══██╗
███████║██║   ██║██████╔╝███████║
██╔══██║██║   ██║██╔══██╗██╔══██║
██║  ██║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

Autonomous  ·  Unified  ·  Reasoning  ·  Agent
```

<p align="center">
  <strong>The most complete open-source autonomous personal AI agent stack.</strong><br>
  Runs 24/7 on your Mac. Talks via Telegram and live voice. Thinks, remembers, and improves itself.
</p>

<br>

---

## Why AURA is Different

Most "personal AI" setups are glorified chatbots. AURA is a production-grade autonomous system that:

- **Costs $0/month for most usage** — 11-brain cascade routes every request to the cheapest capable model first. Free local models handle ~80% of requests before touching subscription APIs.
- **Has real memory** — your entire Obsidian vault (11k+ chunks) is indexed semantically. Every response draws from your own notes, automatically.
- **Speaks and listens in real-time** — Gemini 2.5 Flash Native Audio daemon runs bidirectional live audio. No transcription pipeline, no latency.
- **Two-agent mesh** — AURA + Hermes work as a team. Delegate, parallelize, share memory across two independent stacks.
- **Generates images locally** — FLUX.1-dev via ComfyUI on your own hardware. No per-image cost, no API rate limits.
- **Self-improving** — the conductor loop analyzes its own codebase every 15 minutes, generates improvement tasks, and commits fixes automatically.
- **No SDK dependency** — drives `claude` CLI via subprocess. Your subscription covers everything. Zero per-message API billing.

---

## Capabilities vs Other Agents

| Capability | Typical AI assistant | AURA |
|---|---|---|
| 24/7 autonomous operation | ✗ | ✅ macOS LaunchAgent, KeepAlive, watchdog |
| Semantic memory over personal notes | ✗ | ✅ Obsidian RAG — 11k+ chunks, local embeddings |
| Real-time voice (no STT/TTS pipeline) | ✗ | ✅ Gemini 2.5 Flash Native Audio — bidirectional |
| Two-agent coordination | ✗ | ✅ AURA + Hermes mesh, shared memory vault |
| Local image generation (FLUX.1-dev) | ✗ | ✅ ComfyUI on your hardware — no cloud cost |
| Social media publishing | ✗ | ✅ Instagram via Meta Graph API |
| Branded email (SMTP) | ✗ | ✅ Ionos direct — quotes, templates, auto-send |
| Self-improvement loop | ✗ | ✅ Conductor: analyze → implement → verify → commit |
| Zero-cost brain routing | ✗ | ✅ 11 brains, free-first cascade |
| Knowledge analytics | ✗ | ✅ DuckDB pipeline over all indexed content |
| Web-aware design generation | ✗ | ✅ open-design carousels, HTML posts |
| Mobile terminal access | ✗ | ✅ Termora PTY — one-link browser terminal |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  macOS LaunchAgent — KeepAlive, ThrottleInterval=10s        │
├─────────────────────────────────────────────────────────────┤
│  Python process  ·  src/main.py                             │
│  + Watchdog (2-min ping, 3-strike auto-restart)             │
├─────────────────────────────────────────────────────────────┤
│  Conductor Loop — 15-min autonomous cycle                   │
│  analyze codebase → generate tasks → implement → verify     │
├─────────────────────────────────────────────────────────────┤
│  Brain Router  ·  AuraCortex (EMA self-learning scores)     │
│  ┌──────────────┬──────────────────┬──────────────────┐    │
│  │  zero-token  │  free brains     │  subscription    │    │
│  │  (no LLM)    │  qwen/gemini/... │  haiku → sonnet  │    │
│  └──────────────┴──────────────────┴──────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  RAG Context Injection — build_system_prompt_async()        │
│  ├── ~/Obsidian vault  (11k+ chunks, semantic search)       │
│  ├── ~/.aura/memory/   (persistent state files)             │
│  └── Telegram history  (indexed after every exchange)       │
├─────────────────────────────────────────────────────────────┤
│  Tool Manifest — live TCP port detection at call time       │
│  open-design · ComfyUI · Termora · Hermes                   │
├─────────────────────────────────────────────────────────────┤
│  Knowledge Pipeline — ~/.aura/knowledge_lake/               │
│  DuckDB → keywords · source_summary · conversations         │
├─────────────────────────────────────────────────────────────┤
│  FastAPI :${API_SERVER_PORT} + SSE Dashboard                │
└─────────────────────────────────────────────────────────────┘

Voice daemon (parallel, port 8085):
Gemini 2.5 Flash Native Audio ↔ same tool registry as Telegram
```

---

## The 11-Brain Cascade

Every request hits the cheapest capable brain first. AuraCortex (EMA scoring) learns which brain handles which intent best and builds bypass rules over time.

| # | Brain | Cost | Best for |
|---|---|---|---|
| 1 | `zero-token` | $0 | Bash, git, file ops — no LLM needed |
| 2 | `api-zero` | $0 | Weather, crypto, QR via free public APIs |
| 3 | `ollama-local` | $0 | Local Qwen/Llama on your hardware |
| 4 | `ollama-remote` | $0 | Remote LAN Ollama server |
| 5 | `qwen-code` | $0 | Alibaba Qwen Code CLI, 1k req/day |
| 6 | `opencode` | $0 | OpenCode CLI + OpenRouter free |
| 7 | `gemini` | $0 | Google Gemini CLI, free tier, web search |
| 8 | `openrouter` | $0 | Free models (pressure fallback) |
| 9 | `cline` | $0 | Local Ollama via Cline |
| 10 | **`haiku`** | subscription | **Primary** — chat, translate, reasoning |
| 11 | `sonnet` | subscription | Complex tasks, long context |

**AuraCortex** — self-learning EMA layer. After 2+ failures for a brain/intent pair, it creates a bypass rule. All scores persist to `~/.aura/cortex.json`. CHAT/TRANSLATE hits Haiku directly. CODE starts with local models.

---

## Voice Agent — Gemini 2.5 Flash Native Audio

The voice daemon is a second instance of AURA running on port 8085. It connects to Google's Gemini 2.5 Flash Native Audio model — **bidirectional real-time audio, no STT/TTS pipeline**.

```
Microphone → Gemini Live WebSocket → Tool registry → Speaker
```

Key properties:
- Same tool registry as Telegram — any `@aura_tool` decorated function works in voice
- Session auto-reconnects on drop (Gemini Live sessions expire after extended idle)
- Sleep state preserved across watchdog restarts — no unexpected wakeups
- Manual sleep/wake: `curl -X POST http://localhost:8085/sleep|wake`
- Sleeping by default — wakes on demand

---

## Hermes Mesh — Two-Agent Coordination

AURA pairs with a sibling agent (**Hermes**, OpenClaw/Node.js) for tasks that benefit from parallelism or different capabilities.

```
AURA (Claude/Python)          Hermes (Groq/Node.js)
Port 3002                     Port 18789

AURA → Hermes: REST API
Hermes → AURA: MCP aura__* tools
Both: shared ~/.aura/memory/shared/ vault
```

| AURA specializes in | Hermes specializes in |
|---|---|
| Local filesystem + bash | Web search (DuckDuckGo native) |
| ComfyUI image generation | Browser control |
| Email (Ionos SMTP) | Lossless long-context sessions |
| Git commits | Native cron jobs |
| Instagram publish | 131k token context window |

Shared memory at `~/.aura/memory/shared/` — both agents read and write the same files. Changes are visible to both within seconds.

---

## RAG Memory — Obsidian + Semantic Search

Every LLM call is enriched with the most relevant 1,500 characters from your entire knowledge base — **automatically, with no prompting required**.

```python
# Happens before every brain call:
context = await build_system_prompt_async(user_message)
# → runs cosine similarity search over 11k+ embeddings
# → prepends most relevant chunks to system prompt
```

- **Embeddings**: `nomic-embed-text` via Ollama — 768-dim, fully local, no cloud calls
- **Store**: SQLite at `~/.aura/rag.db`
- **Sources**: your Obsidian vault · AURA memory files · source code · Telegram history
- **Re-index**: every 5 minutes, content-hash based — only re-embeds changed files
- **Speed**: ~50ms per retrieval at 11k chunks

---

## Knowledge Pipeline — DuckDB Analytics

```bash
# Build all Parquet tables from your indexed content (~3 seconds)
uv run python -m src.spark.pipeline

# Query top keywords across all your memory
uv run python -m src.spark.pipeline --query keywords --top 20

# Most active knowledge sources
uv run python -m src.spark.pipeline --query source_summary

# Dry run — see what would be built
uv run python -m src.spark.pipeline --dry-run
```

Output tables at `~/.aura/knowledge_lake/`:

| Table | Content |
|---|---|
| `keywords.parquet` | Word frequency by source type |
| `source_summary.parquet` | Chunk count + chars + last updated per source |
| `recent_memory.parquet` | Latest 200 memory + Obsidian chunks |
| `conversations.parquet` | All indexed Telegram exchanges |

DuckDB runs with no JVM, no cluster. Architecture is PySpark-compatible for future scale.

---

## Self-Improvement Loop — The Conductor

AURA modifies its own codebase. Every 15 minutes:

```
1. Analyze  — scan own source for issues, patterns, dead code
2. Plan     — generate prioritized fix tasks
3. Implement — write code changes (via claude CLI)
4. Verify   — run pytest; auto-revert on failure
5. Commit   — structured git commit if tests pass
```

**Nine core files are permanently protected** — the conductor can never touch them:

```python
_PROTECTED_CORE_FILES = frozenset({
    "src/infra/proactive_loop.py", "src/infra/watchdog.py",
    "src/main.py", "src/config/settings.py",
    "src/brains/conductor.py", "src/brains/router.py",
    "src/mcp/cli_registrar.py", "src/bot/orchestrator.py",
})
```

After every conductor commit, pytest runs automatically. Failure = auto-revert. The conductor never runs `git add -A` — only stages explicit files. Secret patterns are always filtered before staging.

---

## Tool Auto-Discovery

Any function decorated with `@aura_tool` in `src/actions/tools/*.py` is automatically:
- Registered in the MCP server (available to other Claude Code instances)
- Available to the Telegram brain via tool manifest
- Available to the voice agent via ToolExecutor registry

No imports, no registration calls needed:

```python
# src/actions/tools/my_tool.py
from src.actions.registry import aura_tool

@aura_tool
async def my_new_tool(param: str) -> str:
    """What this tool does — shows up in tool manifest automatically."""
    return f"result: {param}"
```

---

## Email — Ionos SMTP

Send branded emails directly from Telegram or voice commands:

```python
# General email (auto-registered as AURA tool)
rud_email_send(to, subject, body, html=None, reply_to=None)

# HTML quote with full branding (black/gold design)
rud_email_presupuesto(
    to, cliente_nombre, proyecto,
    items=[{"descripcion": "...", "precio": 500}],
    total=500, validez_dias=30
)

# Check SMTP configuration
rud_email_status()
```

Transport: `smtp.ionos.es:587` + STARTTLS. Configure `IONOS_EMAIL_USER` and `IONOS_EMAIL_PASS` in `.env`.

---

## Installation

**Requirements**: Python 3.11+, `uv`, `claude` CLI authenticated, Ollama with `nomic-embed-text`.

```bash
git clone https://github.com/royaluniondesign-sys/aura-agent
cd aura-agent
uv install

cp .env.example .env
# Required:
# TELEGRAM_BOT_TOKEN=...        (from @BotFather)
# APPROVED_DIRECTORY=/Users/yourname
# ALLOWED_USERS=your-telegram-id

# Local embeddings (required for RAG)
brew install ollama
ollama pull nomic-embed-text

# Install as macOS LaunchAgent (auto-start on boot)
cp src/infra/com.aura.bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.aura.bot.plist
```

**Recommended `.env` additions:**

```bash
# Brain cascade
OPENROUTER_API_KEY=sk-or-...       # Free models fallback
GEMINI_API_KEY=AIzaSy...           # Gemini brain + voice STT
NVIDIA_API_KEY=nvapi-...           # FLUX.1 image generation

# Notifications
OWNER_CHAT_ID=your-telegram-id     # Watchdog alerts

# Social
META_ACCESS_TOKEN=...              # Instagram publishing
INSTAGRAM_HANDLE=@your_handle

# Email
IONOS_EMAIL_USER=hello@yourdomain.com
IONOS_EMAIL_PASS=your-smtp-password

# API server
API_SERVER_PORT=3002               # Dashboard + webhooks
AGENTIC_MODE=true                  # Natural language mode (default)
```

**Dev commands:**

```bash
uv run make dev        # Install all deps including dev
uv run make run        # Run the bot
uv run make test       # 498 tests + coverage report
uv run make lint       # black + isort + flake8 + mypy
uv run make format     # Auto-format
```

---

## Configuration Reference

All settings via environment variables (Pydantic Settings v2). See `.env.example` for full list.

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | From @BotFather |
| `APPROVED_DIRECTORY` | ✅ | Root directory for file operations |
| `ALLOWED_USERS` | ✅ | Comma-separated Telegram user IDs |
| `AGENTIC_MODE` | — | `true` (default) — natural language mode |
| `API_SERVER_PORT` | — | `3002` (default) — dashboard + webhooks |
| `GEMINI_API_KEY` | — | Gemini brain + voice transcription |
| `OPENROUTER_API_KEY` | — | Free model fallback |
| `NVIDIA_API_KEY` | — | FLUX.1 image generation |
| `OWNER_CHAT_ID` | — | Watchdog + conductor Telegram alerts |
| `IONOS_EMAIL_USER` | — | SMTP sender address |
| `IONOS_EMAIL_PASS` | — | SMTP password |
| `INSTAGRAM_HANDLE` | — | Default Instagram account handle |
| `META_ACCESS_TOKEN` | — | Instagram publishing |
| `HERMES_API_URL` | — | Sibling agent endpoint |
| `AURA_HOME` | — | Project root for brain health checks |

---

## Security Model

**Five layers, always active:**

1. **Auth** — Telegram user ID whitelist. Unknown users get no response.
2. **Isolation** — all file ops sandboxed to `APPROVED_DIRECTORY`. Path traversal blocked.
3. **Input validation** — blocks `;`, `&&`, `$()`, backticks, `..` traversal, secrets file access.
4. **Rate limiting** — per-user token bucket.
5. **Audit log** — every action recorded in SQLite with risk scoring.

**Conductor protection:**
- 9 core files in immutable denylist
- After every commit: pytest runs, auto-revert on failure
- Secret file filter: `.env`, `credential`, `token`, `password` always skipped
- Never uses `git add -A`

See [SECURITY.md](SECURITY.md) for full threat model, webhook authentication, and production hardening checklist.

---

## Project Layout

```
src/
├── brains/           11 brain implementations + Cortex router + Conductor
│   ├── cortex.py     EMA self-learning routing (persists to cortex.json)
│   ├── router.py     Intent → brain mapping
│   ├── conductor/    Autonomous loop: planner, executor, verifier
│   └── *_brain.py    Individual brain implementations
├── context/          System prompt construction + RAG injection
├── rag/              Local vector search (Ollama, SQLite, cosine sim)
├── spark/            Knowledge analytics (DuckDB → Parquet)
├── economy/          Intent classification (regex + semantic)
├── infra/            Proactive loop, watchdog, auto-executor, LaunchAgent
├── scheduler/        APScheduler cron + routines store
├── bot/              Telegram handlers, middleware, orchestrator
├── claude/           Claude CLI facade + session management
├── api/              FastAPI server + SSE dashboard (:API_SERVER_PORT)
├── storage/          SQLite repositories (sessions, audit, costs)
├── security/         Auth, input validation, rate limiting
├── events/           Async pub/sub EventBus
├── notifications/    Rate-limited Telegram delivery
├── integrations/     ionos_client, gmail, comfyui, n8n, publication_db
├── actions/tools/    @aura_tool auto-discovered tools
├── workflows/        Content pipeline, social publish, email, blog
└── voice/            Gemini Live daemon + TTS + screen/computer tools
dashboard/            Single-file SSE dashboard (10 real-time panels)
tests/                498 tests — unit + integration
```

**Key data paths** (configure via env or accept defaults):

```
~/.aura/rag.db              SQLite vector store (11k+ chunks)
~/.aura/knowledge_lake/     DuckDB Parquet tables
~/.aura/memory/             Persistent AURA state (markdown files)
~/.aura/cortex.json         Self-learned brain routing scores
~/.aura/social_drafts/      Image queue for publishing
```

---

## Tech Stack

| Component | Library |
|---|---|
| Language | Python 3.11–3.13 |
| Telegram | python-telegram-bot 22.x |
| Voice | google-genai (Gemini 2.5 Flash Native Audio) |
| API server | FastAPI + uvicorn |
| Scheduler | APScheduler |
| Database | SQLite + aiosqlite |
| Embeddings | Ollama nomic-embed-text (768-dim, local) |
| Analytics | DuckDB 1.5.x |
| Email | smtplib + STARTTLS (Ionos) |
| Logging | structlog (JSON prod / console dev) |
| Deps | uv |
| Claude interface | `claude` CLI subprocess (subscription auth, no SDK) |

---

## Roadmap

| Feature | Status |
|---|---|
| Cross-context bridge (Telegram ↔ Voice shared state) | 🔶 Planned |
| Voice → Telegram auto-notify after tool execution | 🔶 Planned |
| Knowledge lake scheduler (auto every 6h) | 🔶 Planned |
| Video pipeline (Wan2.1 → Reels/TikTok) | 🔶 Planned |
| mem0 vector store (replace SQLite cosine) | 🔶 Planned |
| Test coverage 23% → 80% | 🔄 In progress |

---

## Current Status

| Metric | Value |
|---|---|
| Version | 0.11.1 |
| Tests | 498 passing · 23% coverage |
| Primary brain | Claude Haiku (subscription) |
| Voice | Gemini 2.5 Flash Native Audio |
| RAG | 11,008 chunks indexed · 5-min re-index |
| Knowledge lake | 4 Parquet tables · ~3s build |
| Stability | Beta — brain routing, RAG, voice production-stable |

---

## License

MIT — see [LICENSE](LICENSE).

© 2026 [Royal Union Design](https://rud-web.vercel.app)

---

<p align="center">
  <strong>AURA — your hardware, your models, your rules.</strong><br>
  <em>Built autonomously. Improved continuously.</em>
</p>
