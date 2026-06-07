# AiOS — Mapa del Sistema
*Actualizado: 2026-06-07*

## Estructura de carpetas canónica

```
~/aura/                          ← EL ÚNICO PROYECTO (Python)
├── src/
│   ├── main.py                  ← Entrypoint bot Telegram
│   ├── bot/                     ← Handlers Telegram
│   ├── brains/                  ← Router + Cortex EMA + Conductor
│   ├── context/aura_context.py  ← build_system_prompt_async() — RAG + tool manifest
│   ├── actions/tools/           ← @aura_tool auto-registradas (16 archivos)
│   ├── infra/                   ← watchdog, proactive_loop, mesh_loop, auto_executor
│   ├── mcp/aura_server.py       ← MCP server stdio (Claude Desktop, Hermes)
│   ├── rag/                     ← Obsidian indexing, embeddings Ollama
│   ├── voice/voice_daemon.py    ← AURA Voz — Gemini 2.5 Flash Live Audio (puerto 8085)
│   └── social/                  ← Instagram, scheduling, publisher
├── menubar/aura_bar.py          ← Menubar macOS (rumps)
├── .venv/                       ← Python 3.13, deps instaladas
├── .env                         ← Config (TELEGRAM_BOT_TOKEN, etc.)
├── logs/                        ← bot.stdout.log, voice-agent.stdout.log
└── docs/                        ← Esta carpeta

~/.aura/                         ← DATOS en runtime (no tocar desde código)
├── memory/                      ← Memoria persistente cross-session
├── rag.db                       ← Base de datos RAG (SQLite + embeddings)
├── knowledge_lake/              ← DuckDB Parquet pipeline
└── social_drafts/               ← Borradores de posts

~/.openclaw/                     ← HERMES (Node.js/OpenClaw — no mezclar con aura)
├── openclaw.json                ← Config principal Hermes
└── workspace/                   ← Workspace Hermes + memory symlinks
```

## Servicios y LaunchAgents

| LaunchAgent | Puerto | Qué hace | Auto-restart |
|---|---|---|---|
| com.aura.telegram-bot | 3002 | AURA bot (@rudagency_bot) | KeepAlive:true |
| com.aura.voice-agent | 8085 | AURA Voz — Gemini Live | KeepAlive:SuccessfulExit=false |
| com.aura.menubar | — | Icono menubar macOS | KeepAlive:true |
| com.aura.comfyui | 8188 | FLUX.1-dev image gen | KeepAlive:SuccessfulExit=false |
| com.aura.dashboard-tunnel | — | ngrok tunnel al dashboard | KeepAlive:SuccessfulExit=false |
| com.aura.cleanup-ram | — | Cron: liberar RAM cada 6h | — |
| com.aura.log-rotation | — | Cron: rotar logs cada día | — |
| com.hermes.openclaw | 18789 | Hermes bot (@rudserverbot) | KeepAlive:SuccessfulExit=false |
| com.termora.agent | 4030 | Terminal web Node.js | KeepAlive:SuccessfulExit=false |

## Bots Telegram

| Bot | Handle | Brain | Stack |
|---|---|---|---|
| AURA | @rudagency_bot | Claude (claude-agent-sdk via CLI) | Python ~/aura/ |
| Hermes | @rudserverbot | Groq/Cerebras/OpenRouter free | Node.js OpenClaw |

## Reglas absolutas

- **Zero cost extra** — Claude: MAX plan subscription via CLI. Hermes: free tiers (Groq/Cerebras/Ollama/Google)
- **Una sola carpeta de código**: `~/aura/` para todo Python. `~/.openclaw/` para Hermes (no mezclar)
- **Configuración persiste** via LaunchAgents + .env + ~/.aura/memory/
- **No instalar deps globalmente** — siempre en ~/aura/.venv/
