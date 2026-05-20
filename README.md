<p align="center">
  <img src="https://img.shields.io/badge/AURA-v0.11.0-d97757?style=for-the-badge&labelColor=0e0d0c&logoColor=d97757" alt="AURA v0.11.0">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776ab?style=for-the-badge&labelColor=0e0d0c" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Tests-498_passing-22c55e?style=for-the-badge&labelColor=0e0d0c" alt="498 passing">
  <img src="https://img.shields.io/badge/Brain-Haiku_%2F_Gemini-7c5cff?style=for-the-badge&labelColor=0e0d0c" alt="Haiku / Gemini">
  <img src="https://img.shields.io/badge/RAG-11k%2B_chunks-f59e0b?style=for-the-badge&labelColor=0e0d0c" alt="11k+ chunks">
  <img src="https://img.shields.io/badge/License-MIT-475569?style=for-the-badge&labelColor=0e0d0c" alt="MIT">
</p>

<br>

```
   ██████╗ ██╗   ██╗██████╗  █████╗
  ██╔══██╗██║   ██║██╔══██╗██╔══██╗
  ███████║██║   ██║██████╔╝███████║
  ██╔══██║██║   ██║██╔══██╗██╔══██║
  ██║  ██║╚██████╔╝██║  ██║██║  ██║
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

  Autonomous  ·  Unified  ·  Reasoning  ·  Agent
```

<p align="center">
  <strong>A personal AI agent that lives on your Mac, runs 24/7, and thinks for itself.</strong><br>
  Talk to it from your phone. It executes, remembers, and improves — without you watching.
</p>

<br>

---

## What is AURA

AURA is a self-directing AI agent running as a macOS LaunchAgent, reachable from anywhere via Telegram. You send a message — in any language — and AURA decides how to handle it: run a bash command instantly, pull semantic context from your Obsidian vault, speak back to you in real-time, generate an image, publish to Instagram, or send a branded email quote to a client.

**Two channels. One brain.**

| Channel | Transport | Model |
|---|---|---|
| 💬 **Telegram** (`@rudagency_bot`) | python-telegram-bot | Claude Haiku → Sonnet |
| 🎙 **Voice** (always-on daemon) | Gemini 2.5 Flash Native Audio | Gemini Live bidirectional |

Both channels share the same tool registry, same memory, same identity. A tool registered once works across Telegram commands and live voice sessions without any extra wiring.

**No Anthropic SDK. No per-message billing.**  
AURA drives the `claude` CLI via subprocess. Your Claude subscription covers everything.

---

## What AURA Can Do That Claude Alone Can't

| Capability | Claude chat | AURA |
|---|---|---|
| 24/7 autonomous operation | ✗ | ✅ LaunchAgent, KeepAlive, auto-restart |
| Obsidian vault memory | ✗ | ✅ 11k+ chunks, semantic search |
| Voice — real-time bidirectional | ✗ | ✅ Gemini 2.5 Flash Native Audio |
| Scheduled & proactive tasks | ✗ | ✅ APScheduler + 15-min conductor loop |
| Local filesystem access | ✗ | ✅ read/write any file on your Mac |
| Image generation (FLUX.1-dev) | ✗ | ✅ ComfyUI local or Pollinations.ai |
| Instagram publishing | ✗ | ✅ Meta Graph API, one natural command |
| Email (Ionos SMTP) | ✗ | ✅ Branded quotes, templates, direct send |
| Design generation | ✗ | ✅ open-design carousels and posts |
| Hermes agent mesh | ✗ | ✅ two-agent coordination, shared memory |
| Self-improvement loop | ✗ | ✅ conductor scans + auto-commits fixes |
| Cost routing (free first) | ✗ | ✅ 11 brains, $0 for most tasks |
| Knowledge analytics | ✗ | ✅ DuckDB pipeline over all memory |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 0 — macOS LaunchAgent (KeepAlive, ThrottleInterval)  │
├─────────────────────────────────────────────────────────────┤
│  Layer 1 — Python process  ·  src/main.py                   │
│            + Watchdog ping (2-min, 3-strike SIGTERM)        │
├─────────────────────────────────────────────────────────────┤
│  Layer 2 — Conductor / Proactive Loop  ·  15-min cycle      │
│            analyze → implement → verify → commit            │
├─────────────────────────────────────────────────────────────┤
│  Layer 3 — Brain Router  ·  AuraCortex (EMA scoring)        │
│  ┌──────────────┬───────────────────┬──────────────────┐   │
│  │  zero-token  │  free-tier brains │  subscription    │   │
│  │ bash/git/ops │ qwen/gemini/ollama│ haiku → sonnet   │   │
│  └──────────────┴───────────────────┴──────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Layer 4 — RAG Context Injection  ·  build_system_prompt_async()  │
│  ├── ~/Obsidian/**/*.md  (11k+ chunks)                      │
│  ├── ~/.aura/memory/*.md  (persistent state)                │
│  ├── MISSION.md + CLAUDE.md  (identity)                     │
│  └── Telegram conversation history                          │
├─────────────────────────────────────────────────────────────┤
│  Layer 4.5 — Tool Manifest  ·  live TCP port checks         │
│  ├── open-design :59826  →  carousel/post generation        │
│  ├── ComfyUI :8188        →  FLUX.1-dev images (~90s)       │
│  └── Termora :4030        →  mobile terminal URL            │
├─────────────────────────────────────────────────────────────┤
│  Layer 5 — Knowledge Pipeline  ·  ~/.aura/knowledge_lake/   │
│  └── DuckDB: keywords · source_summary · conversations      │
├─────────────────────────────────────────────────────────────┤
│  Layer 6 — FastAPI :3002 + Dashboard (SSE real-time)        │
└─────────────────────────────────────────────────────────────┘

Voice daemon runs in parallel on port 8085 — Gemini 2.5 Flash
Native Audio, sleeping by default, same tool registry.
```

**Supporting systems (always-on):**

| System | Interval | What it does |
|---|---|---|
| `AutoExecutor` | 5 min | Picks up pending generated tasks |
| `SelfEvaluator` | 30 min | Scans codebase, auto-creates fix tasks |
| `RAGIndexer` | 5 min | Re-indexes changed content (content-hash) |
| `EventBus` | async | Webhooks → agent → Telegram notifications |

---

## Brain Cascade — Cost-First Routing

| Brain | Cost | Primary use |
|---|---|---|
| `zero-token` | $0 | Bash, git, file ops — no LLM, instant |
| `api-zero` | $0 | Weather, crypto, QR codes via public APIs |
| `ollama-rud` | $0 | Remote LAN Ollama (code-focused) |
| `qwen-code` | $0 | Alibaba Qwen Code CLI, 1k req/day |
| `opencode` | $0 | OpenCode CLI + OpenRouter backend |
| `gemini` | $0 | Google Gemini CLI, free tier, web-grounded |
| `openrouter` | $0 | Free model (pressure fallback only) |
| `cline` | $0 | Local Ollama via Cline |
| **`haiku`** | subscription | **Primary** — chat, translate, general |
| `sonnet` | subscription | Complex reasoning, long tasks |
| `opus` | subscription | Maximum reasoning quality |

**Intent → Brain map:**

| Intent | Brain |
|---|---|
| `CHAT`, `TRANSLATE` | Haiku |
| `CODE` | ollama-rud → qwen → haiku cascade |
| `SEARCH` | Gemini |
| `SHELL` | zero-token (no LLM) |
| `IMAGE` | image-brain (ComfyUI / Pollinations) |
| `DESIGN` | open-design tool |
| `SOCIAL` | instagram_publish pipeline |

**AuraCortex**: self-learning EMA layer. Tracks success rate and latency per brain per intent. Creates bypass rules after 2+ failures. Persists to `~/.aura/cortex.json`.

---

## Voice Agent — Gemini 2.5 Flash Native Audio

AURA Voice runs as a separate daemon on port 8085. It uses Google's Gemini 2.5 Flash Native Audio for real-time bidirectional audio — no STT/TTS pipeline, no latency from transcription.

```
Microphone → Gemini Live session → AURA tool registry → Speaker
```

- **Model**: `gemini-2.5-flash-native-audio-preview`
- **Language**: Spanish primary, auto-detects English
- **Tools**: same registry as Telegram — rud_email_send, instagram_publish, bash_run, memory_search, etc.
- **Sleep/wake**: manual via Telegram or voice command (disabled media_watch auto-wake — was triggering on window switches)
- **Session continuity**: Gemini sessions auto-reconnect on drop; sleep state preserved across restarts

```bash
# Via Telegram
/voice wake    # wake from sleep
/voice sleep   # go back to sleep
/voice status  # check state

# Via curl
curl -X POST http://localhost:8085/wake
curl -X POST http://localhost:8085/sleep
curl http://localhost:8085/status
```

---

## Hermes Mesh — Two-Agent Coordination

AURA has a sibling agent: **Hermes** (`@rudserverbot`, OpenClaw/Node.js, port 18789). Same owner, different stack, complementary capabilities.

```
AURA ←──────────────────────────────→ Hermes
@rudagency_bot                         @rudserverbot
Claude Haiku/Sonnet                    Groq llama-3.3-70b
Port 3002                              Port 18789

AURA → Hermes:  curl http://localhost:18789/
Hermes → AURA:  MCP aura__* tools (bash_run, git_*, instagram_publish…)
```

**Shared memory** (`~/.aura/memory/shared/`):
- `tasks.md` — pending tasks for both agents
- `projects.md` — active projects
- Symlinked into Hermes workspace — both read the same files

| AURA has | Hermes has |
|---|---|
| ComfyUI image generation | Browser control (port 18791) |
| Ionos email direct | Web search (DuckDuckGo native) |
| Instagram publish | Cron jobs native |
| Git commit native | 131k context window |
| Obsidian RAG | Lossless compaction |

---

## Email — RUD Studio

AURA can send email from `hello@royaluniondesign.com` directly, with full HTML branding.

Three auto-registered tools (work in Telegram and Voice):

```python
# General email
rud_email_send(to, subject, body, html=None, reply_to=None)

# Branded HTML quote — black/gold RUD design
rud_email_presupuesto(to, cliente_nombre, proyecto, items, total, validez_dias)
# items = [{"descripcion": "...", "precio": 500}, ...]

# Check SMTP config
rud_email_status()
```

**SMTP**: smtp.ionos.es:587 with STARTTLS. Client at `src/integrations/ionos_client.py`.

---

## RAG Memory — Obsidian + Semantic Search

Every brain call is enriched with the most relevant 1,500 chars from your entire knowledge base — automatically.

- **Embeddings**: `nomic-embed-text` via Ollama, 768-dim, fully local
- **Store**: SQLite at `~/.aura/rag.db` — 11,000+ chunks
- **Sources**: Obsidian vault · AURA memory · MISSION.md · source code · Telegram history
- **Auto re-index**: every 5 minutes, content-hash based (skips unchanged)
- **Injection**: `build_system_prompt_async(user_message)` runs before every LLM call

---

## Knowledge Pipeline — DuckDB Analytics

```bash
# Dry run — count chunks by type
uv run python -m src.spark.pipeline --dry-run

# Build all Parquet tables (~3 seconds for 11k chunks)
uv run python -m src.spark.pipeline

# Query top keywords
uv run python -m src.spark.pipeline --query keywords --top 20

# Most active sources
uv run python -m src.spark.pipeline --query source_summary --top 10
```

Tables at `~/.aura/knowledge_lake/`: `keywords.parquet` · `source_summary.parquet` · `recent_memory.parquet` · `conversations.parquet`

Engine: DuckDB (no JVM, ~3s for 11k chunks). Architecture is PySpark-compatible for cluster scale.

---

## Security

**Five layers:**

1. **Authentication** — Telegram user ID whitelist. No unknown users.
2. **Directory isolation** — all file ops sandboxed to `APPROVED_DIRECTORY`.
3. **Input validation** — blocks `;`, `&&`, `$()`, backticks, path traversal.
4. **Rate limiting** — per-user token bucket.
5. **Audit logging** — every action in SQLite.

**Conductor denylist** — nine core engine files never auto-staged or auto-committed:

```python
_PROTECTED_CORE_FILES = frozenset({
    "src/infra/proactive_loop.py", "src/infra/watchdog.py",
    "src/main.py", "src/config/settings.py", "src/config/features.py",
    "src/brains/conductor.py", "src/brains/router.py",
    "src/mcp/cli_registrar.py", "src/bot/orchestrator.py",
})
```

After every conductor commit: pytest runs automatically. Auto-revert on failure.

See [SECURITY.md](SECURITY.md) for full threat model and production checklist.

---

## Installation

**Requirements:** Python 3.11+, `uv`, `claude` CLI authenticated, Ollama with `nomic-embed-text`.

```bash
git clone https://github.com/royaluniondesign-sys/claude-code-telegram
cd claude-code-telegram
uv install

cp .env.example .env
# Required:
# TELEGRAM_BOT_TOKEN=...
# APPROVED_DIRECTORY=/Users/yourname
# ALLOWED_USERS=your-telegram-id

# Embeddings
brew install ollama
ollama pull nomic-embed-text

# Install as LaunchAgent (macOS)
cp src/infra/com.aura.bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.aura.bot.plist
```

**Key optional env vars:**

```bash
API_SERVER_PORT=3002         # Dashboard + webhook API
AGENTIC_MODE=true            # Natural language mode (default)
GEMINI_ENABLED=true          # Enable Gemini brain
OPENROUTER_API_KEY=sk-or-... # Fallback free models
NOTIFICATION_CHAT_IDS=...    # Telegram IDs for proactive alerts
IONOS_EMAIL_USER=...         # hello@yourdomain.com
IONOS_EMAIL_PASS=...         # SMTP password
```

**Dev commands:**

```bash
uv run make dev        # install all deps
uv run make run        # run the bot
uv run make test       # 498 tests + coverage
uv run make lint       # black + isort + flake8 + mypy
uv run make format     # auto-format
```

---

## Project Layout

```
src/
├── brains/           Brain implementations + Cortex + router
│   ├── cortex.py     EMA self-learning routing layer
│   ├── router.py     Intent → brain map
│   └── conductor.py  3-layer autonomous loop
├── context/          System prompt construction + RAG injection
├── rag/              Local vector search (Ollama embeddings)
├── spark/            Knowledge analytics (DuckDB → Parquet)
├── economy/          Intent classification
├── infra/            Proactive loop, watchdog, auto executor
├── scheduler/        APScheduler cron + routines
├── bot/              Telegram handlers, middleware, orchestrator
├── claude/           Claude CLI facade + session management
├── api/              FastAPI server + dashboard routes (:3002)
├── storage/          SQLite repositories
├── security/         Auth, input validation, rate limiting
├── events/           Async pub/sub EventBus
├── notifications/    Rate-limited Telegram delivery
├── integrations/     ionos_client.py + external service clients
├── actions/tools/    @aura_tool auto-discovered tools
│   ├── rud_email.py  Email via Ionos SMTP
│   └── ...
└── voice/            Gemini Live daemon + TTS + screen tools
dashboard/            Real-time dashboard (SSE, 10 panels)
```

**Key paths:**

```
~/.aura/rag.db              Vector store (11k+ chunks)
~/.aura/knowledge_lake/     DuckDB Parquet tables
~/.aura/memory/             Persistent AURA memory (markdown)
~/.aura/cortex.json         Self-learned brain scores
~/.aura/social_drafts/      Images queued for publishing
~/Obsidian/                 Obsidian vault (primary memory)
```

---

## Roadmap

| Feature | Status |
|---|---|
| Cross-context bridge (Telegram ↔ Voice) | 🔶 Planned |
| Voice → Telegram auto-notify after tool calls | 🔶 Planned |
| Knowledge lake scheduler (auto every 6h) | 🔶 Planned |
| Wan2.1 video pipeline → Reels/TikTok | 🔶 Planned |
| mem0 vector store (replace SQLite cosine) | 🔶 Planned |
| Test coverage 23% → 80% | 🔄 In progress |
| Credential rotation (Alibaba, Telegram, Meta) | 🔴 Critical |
| New computer migration | 🔄 In progress |

---

## Tech Stack

| Component | Library |
|---|---|
| Language | Python 3.11–3.13 |
| Telegram | python-telegram-bot 22.x |
| Voice | Gemini 2.5 Flash Native Audio (google-genai) |
| API server | FastAPI + uvicorn |
| Scheduler | APScheduler |
| Database | SQLite + aiosqlite |
| Embeddings | Ollama nomic-embed-text (768-dim, local) |
| Analytics | DuckDB 1.5.x |
| Email | smtplib STARTTLS (Ionos SMTP) |
| Logging | structlog |
| Deps | uv |
| Claude interface | `claude` CLI subprocess (subscription auth) |

---

## Status

| Metric | Value |
|---|---|
| Version | 0.11.0 |
| Tests | 498 passing · 23% coverage |
| Primary brain | Claude Haiku (subscription) |
| Voice brain | Gemini 2.5 Flash Native Audio |
| RAG | 11,008 chunks · 5-min re-index |
| Knowledge lake | 4 Parquet tables · ~3s build |
| Stability | Beta — core routing, RAG, voice production-stable |

---

## License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <strong>AURA — your hardware, your models, your rules.</strong><br>
  <em>Built autonomously. Improved continuously.</em>
</p>
