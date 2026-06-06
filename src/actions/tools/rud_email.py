"""RUD Studio email tools — envía desde IONOS_EMAIL_USER via Ionos SMTP.

Auto-descubierto por MCP y voz. Disponible en Telegram + Voice AURA.
"""

from __future__ import annotations

import os

from src.actions.registry import aura_tool


@aura_tool(
    name="rud_email_send",
    description=(
        "Envía un email profesional desde la cuenta Ionos configurada (IONOS_EMAIL_USER). "
        "Usa para comunicaciones con clientes, presupuestos, seguimiento. "
        "Siempre envía desde la cuenta profesional de RUD Studio."
    ),
    category="email",
    parameters={
        "to": {"type": "str", "description": "Email del destinatario"},
        "subject": {"type": "str", "description": "Asunto del correo"},
        "body": {"type": "str", "description": "Cuerpo en texto plano"},
        "html": {
            "type": "str",
            "description": "Cuerpo HTML opcional (si se da, se usa en lugar de body)",
        },
        "reply_to": {"type": "str", "description": "Reply-To address opcional"},
    },
)
async def rud_email_send(
    to: str,
    subject: str,
    body: str,
    html: str = "",
    reply_to: str = "",
) -> str:
    from src.integrations.ionos_client import send_email

    try:
        await send_email(
            to=to,
            subject=subject,
            body=body,
            html=html or None,
            reply_to=reply_to or None,
        )
        return f"✅ Email enviado a {to} — Asunto: {subject}"
    except Exception as e:
        return f"❌ Error enviando email: {e}"


@aura_tool(
    name="rud_email_presupuesto",
    description=(
        "Envía un presupuesto/propuesta profesional de RUD Studio al cliente. "
        "Genera HTML con branding RUD (negro/dorado). "
        "Incluye: nombre cliente, nombre proyecto, tabla de items con precios, total, validez."
    ),
    category="email",
    parameters={
        "to": {"type": "str", "description": "Email del cliente"},
        "cliente_nombre": {
            "type": "str",
            "description": "Nombre del cliente o empresa",
        },
        "proyecto": {"type": "str", "description": "Nombre del proyecto o servicio"},
        "items": {
            "type": "list",
            "description": "Lista de items: [{'descripcion': '...', 'precio': 1200}]",
        },
        "total": {"type": "float", "description": "Total del presupuesto en EUR"},
        "validez_dias": {
            "type": "int",
            "description": "Días de validez del presupuesto (default 30)",
        },
        "notas": {
            "type": "str",
            "description": "Notas adicionales o condiciones (opcional)",
        },
    },
)
async def rud_email_presupuesto(
    to: str,
    cliente_nombre: str,
    proyecto: str,
    items: list,
    total: float,
    validez_dias: int = 30,
    notas: str = "",
) -> str:
    from src.integrations.ionos_client import send_email

    # Build items rows
    rows = ""
    for item in items:
        desc = item.get("descripcion", item.get("description", str(item)))
        precio = item.get("precio", item.get("price", "—"))
        if isinstance(precio, (int, float)):
            precio = f"{precio:,.0f} €"
        rows += f"""
        <tr>
          <td style="padding:10px 16px;border-bottom:1px solid #1e1e1e;color:#e5e5e5">{desc}</td>
          <td style="padding:10px 16px;border-bottom:1px solid #1e1e1e;color:#c9a84c;text-align:right;font-weight:bold">{precio}</td>
        </tr>"""

    notas_html = (
        f'<p style="margin:16px 0 0;color:#888;font-size:13px">{notas}</p>'
        if notas
        else ""
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f5f0e8;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0e8;padding:40px 0">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#0d0d0d;border-radius:8px;overflow:hidden">
        <!-- Header -->
        <tr><td style="background:#0d0d0d;padding:32px 40px;border-bottom:2px solid #c9a84c">
          <p style="margin:0;font-size:28px;font-weight:900;letter-spacing:4px;color:#f5f0e8">RUD STUDIO</p>
          <p style="margin:4px 0 0;font-size:11px;letter-spacing:3px;color:#c9a84c;text-transform:uppercase">Presupuesto profesional</p>
        </td></tr>
        <!-- Greeting -->
        <tr><td style="padding:32px 40px 0">
          <p style="margin:0;font-size:16px;color:#e5e5e5">Hola <strong style="color:#c9a84c">{cliente_nombre}</strong>,</p>
          <p style="margin:12px 0 0;font-size:14px;color:#999;line-height:1.6">
            Adjunto encontrarás el presupuesto para el proyecto <strong style="color:#e5e5e5">{proyecto}</strong>.
            Hemos preparado esta propuesta pensando en tus objetivos.
          </p>
        </td></tr>
        <!-- Table -->
        <tr><td style="padding:24px 40px 0">
          <table width="100%" cellpadding="0" cellspacing="0" style="border-radius:6px;overflow:hidden;border:1px solid #1e1e1e">
            <tr style="background:#141414">
              <th style="padding:10px 16px;text-align:left;font-size:11px;letter-spacing:2px;color:#666;text-transform:uppercase">Descripción</th>
              <th style="padding:10px 16px;text-align:right;font-size:11px;letter-spacing:2px;color:#666;text-transform:uppercase">Precio</th>
            </tr>
            {rows}
            <tr style="background:#141414">
              <td style="padding:12px 16px;font-size:15px;font-weight:bold;color:#e5e5e5">TOTAL</td>
              <td style="padding:12px 16px;font-size:18px;font-weight:bold;color:#c9a84c;text-align:right">{total:,.0f} €</td>
            </tr>
          </table>
          {notas_html}
        </td></tr>
        <!-- Footer -->
        <tr><td style="padding:32px 40px">
          <p style="margin:0;font-size:13px;color:#666">Validez del presupuesto: <strong style="color:#e5e5e5">{validez_dias} días</strong></p>
          <p style="margin:8px 0 0;font-size:13px;color:#666">Para aceptar o preguntar, responde a este correo.</p>
          <p style="margin:24px 0 0;font-size:12px;color:#444">RUD Studio · {os.environ.get("IONOS_EMAIL_USER", "")}</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    body_plain = (
        f"Hola {cliente_nombre},\n\n"
        f"Presupuesto para: {proyecto}\n\n"
        + "\n".join(
            f"- {i.get('descripcion', i.get('description', str(i)))}: "
            f"{i.get('precio', i.get('price', '—'))} €"
            for i in items
        )
        + f"\n\nTOTAL: {total:,.0f} €"
        + (f"\n\nNotas: {notas}" if notas else "")
        + f"\n\nValidez: {validez_dias} días\n\nRUD Studio · {os.environ.get('IONOS_EMAIL_USER', '')}"
    )

    try:
        await send_email(
            to=to,
            subject=f"Presupuesto — {proyecto} | RUD Studio",
            body=body_plain,
            html=html,
            reply_to=os.environ.get("IONOS_EMAIL_USER", ""),
        )
        return f"✅ Presupuesto enviado a {cliente_nombre} <{to}> — {proyecto} — {total:,.0f} €"
    except Exception as e:
        return f"❌ Error enviando presupuesto: {e}"


@aura_tool(
    name="rud_email_status",
    description="Comprueba si el email Ionos de RUD Studio está configurado y listo para enviar.",
    category="email",
    parameters={},
)
async def rud_email_status() -> str:
    user = os.environ.get("IONOS_EMAIL_USER", "")
    pwd = os.environ.get("IONOS_EMAIL_PASS", "")
    if not user or not pwd:
        return "❌ IONOS_EMAIL_USER / IONOS_EMAIL_PASS no configurados en .env"
    return f"✅ Ionos listo → {user} (SMTP smtp.ionos.com:587)"
