# AiOS — Roadmap por Fases
*Actualizado: 2026-06-07*

## Estado actual: v0.11.0

---

## ✅ Fase 1 — Infraestructura base (COMPLETA)
- Bot Telegram Python operativo
- LaunchAgents para todos los servicios
- Carpeta canónica `~/aura/`
- Bridge AURA↔Hermes bidireccional
- Obsidian vault compartido
- MCP server para Claude Desktop

## ✅ Fase 2 — Social & Contenido (COMPLETA)
- `/social status`, scheduling lenguaje natural
- `social_generate_and_publish` tool autónomo
- Design stack: open-design + DESIGN.md royaluniondesign
- Email templates HTML (bienvenida/presupuesto/newsletter)
- Instagram tokens configurados

## ✅ Fase 3 — Voz & Mesh (COMPLETA)
- AURA Voz: Gemini 2.5 Flash Live Audio (puerto 8085)
- Mesh three-way chat AURA↔Hermes visible en Telegram
- RAG Obsidian: 11k chunks indexados
- Menubar macOS

---

## 🔄 Fase 4 — Producción & Pulido (EN CURSO — v0.12.0)

### Crítico (hacer ya)
- [x] **Rotar credenciales**: TELEGRAM_BOT_TOKEN + META_ACCESS_TOKEN + Alibaba Cloud key (hecho)
- [ ] **Test Instagram end-to-end**: mandar "publica foto de prueba" a AURA y verificar que aparece en @royaluniondesign

### Alto impacto
- [ ] **Testear delegación Hermes→AURA** round-trip real en producción
- [ ] **Email trigger**: Hermes detecta email importante en hello@royaluniondesign.com → notifica AURA
- [ ] **Voice→Telegram auto-notify**: cuando AURA Voz ejecuta tool real → mensaje en Telegram

### Optimización
- [ ] RAG: ampliar a más archivos Obsidian, auto-sync cada hora
- [ ] Conductor loop: revisar que el self-improvement está committeando cambios
- [ ] Auto-executor: verificar que las tareas programadas se ejecutan

---

## 📋 Fase 5 — Expansión (v0.13.0+)
- Video pipeline: Wan2.1 → edición → publicación Reels/TikTok
- mem0 integration real (vectores persistentes cross-session)
- Migración a nuevo ordenador (multi-machine installer)
- Standing Orders Hermes (programas autónomos: digest, monitor)
- Cross-context bridge: Voice → guardar resumen → Telegram

---

## Sesiones Claude Code por fase

Cada fase tiene su propio contexto. Al iniciar una sesión sobre una fase específica:
1. Leer `docs/phases/ROADMAP.md` (este archivo)
2. Leer `docs/architecture/SYSTEM_MAP.md`
3. Leer `docs/runbooks/INCIDENCIAS.md` para no repetir errores
4. Leer `~/.aura/memory/MEMORY.md` para contexto del owner
