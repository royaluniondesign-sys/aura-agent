# Runbook de Incidencias AiOS
*Última actualización: 2026-06-07*

---

## INC-001: Bot AURA no responde en Telegram (2026-06-07)

### Síntoma
AURA (@rudagency_bot) no responde mensajes. El proceso puede estar muerto o crasheando.

### Diagnóstico
```bash
# ¿Está vivo?
launchctl list | grep telegram-bot
ps aux | grep "src.main" | grep -v grep

# ¿Por qué falló?
tail -30 ~/aura/logs/bot.stderr.log
tail -30 ~/aura/logs/bot.stdout.log | grep -E "error|Error|CRITICAL"
```

### Causas conocidas y fixes

**A) `ModuleNotFoundError: No module named 'structlog'`**
→ El venv no tiene deps. Fix:
```bash
cd ~/aura && .venv/bin/pip install -e .
```

**B) `[Errno 48] address already in use` (puerto 3002)**
→ Proceso anterior no terminó. Fix:
```bash
lsof -ti:3002 | xargs kill -9 2>/dev/null
launchctl unload ~/Library/LaunchAgents/com.aura.telegram-bot.plist
launchctl load ~/Library/LaunchAgents/com.aura.telegram-bot.plist
```

**C) Watchdog mata el bot (3 consecutive getMe failures)**
→ RAM alta o red lenta. El LaunchAgent tiene KeepAlive:true → reinicia solo.
→ Si no reinicia: `launchctl kickstart -k gui/$(id -u)/com.aura.telegram-bot`

**D) Bot no arranca en absoluto (LaunchAgent sin PID)**
→ Verificar que el LaunchAgent existe y está correcto:
```bash
cat ~/Library/LaunchAgents/com.aura.telegram-bot.plist
launchctl load ~/Library/LaunchAgents/com.aura.telegram-bot.plist
```

### Prevención aplicada
- `KeepAlive: true` en com.aura.telegram-bot.plist
- Todas las deps en `[project.dependencies]` de pyproject.toml
- Ruta canónica: siempre `~/aura/`

---

## INC-002: Hermes (@rudserverbot) no responde (2026-06-07)

### Síntoma
Hermes recibe mensajes pero no los procesa. Los mensajes quedan como "pending" en getUpdates.

### Diagnóstico
```bash
# ¿Está vivo y conectado?
/opt/homebrew/bin/openclaw channels status

# ¿Cuántos tools tiene?
python3 -c "
import json
with open('/Users/oxyzen/.openclaw/openclaw.json') as f:
    d = json.load(f)
print('MCP servers:', list(d.get('mcp',{}).get('servers',{}).keys()))
"

# Logs de errores
tail -20 ~/.openclaw/logs/hermes-err.log | grep "tools\|FAIL\|error"
```

### Causa raíz (este incidente)
Demasiados MCP servers → 130+ tools → todos los free LLMs fallan con `'tools': maximum number is 128`.

La cascada completa fallaba silenciosamente. El bot procesaba el mensaje eventualmente con `openrouter/openai/gpt-oss-120b:free` pero tardaba horas.

### Fix aplicado
Eliminar MCP servers no esenciales de `~/.openclaw/openclaw.json`:
- ~~comfyui~~ → AURA tiene tool nativa
- ~~firecrawl~~ → Hermes tiene web_search nativo
- ~~playwright~~ → no necesario para chat diario

Quedaron: `aura` + `google-workspace` (~78 tools total).

### Ruta MCP AURA en Hermes
Si ves `ENOENT` o timeout en el MCP aura:
```bash
python3 -c "
import json
with open('/Users/oxyzen/.openclaw/openclaw.json') as f: d = json.load(f)
d['mcp']['servers']['aura']['command'] = '/Users/oxyzen/aura/.venv/bin/python'
d['mcp']['servers']['aura']['cwd'] = '/Users/oxyzen/aura'
with open('/Users/oxyzen/.openclaw/openclaw.json', 'w') as f: json.dump(d, f, indent=2)
"
launchctl unload ~/Library/LaunchAgents/com.hermes.openclaw.plist
launchctl load ~/Library/LaunchAgents/com.hermes.openclaw.plist
```

---

## Checklist tras reinicio de máquina

```bash
# 1. Verificar todos los servicios
launchctl list | grep -E "aura|hermes|termora|comfyui"

# 2. Verificar puertos
python3 -c "
import socket
for port, name in [(3002,'AURA-bot'), (8085,'AURA-voice'), (18789,'Hermes'), (4030,'Termora'), (8188,'ComfyUI')]:
    try:
        socket.create_connection(('127.0.0.1', port), timeout=1)
        print(f'✅ {name}:{port}')
    except: print(f'❌ {name}:{port}')
"

# 3. Si AURA no responde → ver logs
tail -20 ~/aura/logs/bot.stderr.log

# 4. Mandar "hola" a @rudagency_bot y @rudserverbot en Telegram
```
