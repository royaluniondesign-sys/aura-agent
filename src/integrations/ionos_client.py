"""Ionos SMTP client — envía correos desde hello@royaluniondesign.com.

Credentials from env: IONOS_EMAIL_USER, IONOS_EMAIL_PASS
SMTP: smtp.ionos.com:587 (STARTTLS)
"""
from __future__ import annotations

import asyncio
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import structlog

logger = structlog.get_logger()

_SMTP_HOST = "smtp.ionos.es"
_SMTP_PORT = 587
_FROM_NAME = os.environ.get("RUD_NAME", "RUD Studio")


def _get_creds() -> tuple[str, str]:
    user = os.environ.get("IONOS_EMAIL_USER", "")
    pwd = os.environ.get("IONOS_EMAIL_PASS", "")
    if not user or not pwd:
        raise ValueError("IONOS_EMAIL_USER / IONOS_EMAIL_PASS not set in .env")
    return user, pwd


def _send_sync(
    to: str,
    subject: str,
    body: str,
    html: Optional[str],
    reply_to: Optional[str],
) -> dict:
    """Blocking SMTP send — run via asyncio.to_thread."""
    user, pwd = _get_creds()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{_FROM_NAME} <{user}>"
    msg["To"] = to
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.attach(MIMEText(body, "plain", "utf-8"))
    if html:
        msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.send_message(msg)
        logger.info("ionos_email_sent", to=to, subject=subject)

    return {"ok": True, "from": user, "to": to, "subject": subject}


async def send_email(
    to: str,
    subject: str,
    body: str,
    html: Optional[str] = None,
    reply_to: Optional[str] = None,
) -> dict:
    """Send email via Ionos SMTP. Returns {"ok": True} or raises."""
    return await asyncio.to_thread(_send_sync, to, subject, body, html, reply_to)
