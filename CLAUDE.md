# CLAUDE.md — AiOS / AURA
*Proyecto de Ricardo (oxyzen). Leer ANTES de tocar cualquier cosa.*

## Contexto rápido
AURA es el sistema AiOS personal de Ricardo: bot Telegram (@rudagency_bot) + voz + social + mesh con Hermes (@rudserverbot). Todo el código Python vive en `~/aura/`. Hermes vive en `~/.openclaw/` (no mezclar).

## Reglas absolutas
- **Zero cost extra** — Claude: MAX plan subscription via `claude` CLI, jamás API key. Hermes: free tiers (Groq/Cerebras/Ollama/Google Gemini)
- **Una carpeta canónica**: `~/aura/` para todo Python. `~/.openclaw/` para Hermes
- **No tocar** `~/.openclaw/openclaw.json` sin leer `docs/runbooks/INCIDENCIAS.md` primero
- Respuestas en español, cortas y directas

## Antes de cualquier cambio, leer
1. `docs/architecture/SYSTEM_MAP.md` — mapa completo del sistema
2. `docs/runbooks/INCIDENCIAS.md` — errores conocidos y sus fixes
3. `docs/phases/ROADMAP.md` — qué está hecho y qué falta
4. `~/.aura/memory/MEMORY.md` — estado actual y preferencias del owner

## Setup (si el bot no arranca)
```bash
cd ~/aura

# 1. Verificar deps
.venv/bin/python -c "import structlog, telegram, anthropic; print('OK')"

# Si falla → instalar
.venv/bin/pip install -e .

# 2. Arrancar servicio
launchctl load ~/Library/LaunchAgents/com.aura.telegram-bot.plist

# 3. Verificar logs
tail -f ~/aura/logs/bot.stdout.log
```

## Servicios del sistema
| Servicio | Puerto | Comando para ver logs |
|---|---|---|
| AURA bot | 3002 | `tail -f ~/aura/logs/bot.stdout.log` |
| AURA voz | 8085 | `tail -f ~/aura/logs/voice-agent.stdout.log` |
| Hermes | 18789 | `tail -f ~/.openclaw/logs/hermes.log` |
| Termora | 4030 | `curl localhost:4030/api/health` |
| ComfyUI | 8188 | `curl localhost:8188/system_stats` |

## Componentes clave
| Archivo | Qué hace |
|---|---|
| `src/main.py` | Entrypoint — arranca todo |
| `src/brains/router.py` | Routing de intenciones → brain |
| `src/context/aura_context.py` | `build_system_prompt_async()` — RAG + herramientas |
| `src/actions/tools/` | 16 tools @aura_tool (drop a file = auto-registrada) |
| `src/voice/voice_daemon.py` | AURA Voz — Gemini 2.5 Flash Live Audio |
| `src/infra/proactive_loop.py` | Loop autónomo 15min — NO modificar |
| `src/mcp/aura_server.py` | MCP server para Claude Desktop y Hermes |

## Añadir una tool nueva
```python
# src/actions/tools/mi_tool.py
from src.actions.registry import aura_tool

@aura_tool
async def mi_tool(param: str) -> str:
    """Descripción corta — aparece en el manifest."""
    return resultado
```
Auto-registrada. Disponible en Telegram, MCP, y el manifest del contexto.
