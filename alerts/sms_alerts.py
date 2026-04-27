"""Optional SMS alert helper.

This module is intentionally conservative. It does not send SMS unless all
Twilio-related environment variables are configured and ALERTS_ENABLED=true.
"""

from __future__ import annotations

import os


def alerts_enabled() -> bool:
    """Return whether alerts are enabled by environment."""
    return os.environ.get("ALERTS_ENABLED", "false").strip().lower() == "true"


def send_sms_alert(message: str) -> dict[str, str]:
    """Send an SMS alert if Twilio is configured; otherwise return skipped."""
    if not alerts_enabled():
        return {"status": "skipped", "reason": "ALERTS_ENABLED=false"}

    required = [
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_FROM_NUMBER",
        "ALERT_TO_NUMBER",
    ]
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        return {"status": "skipped", "reason": f"Missing variables: {missing}"}

    try:
        from twilio.rest import Client
    except ModuleNotFoundError:
        return {"status": "skipped", "reason": "twilio package not installed"}

    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    sent = client.messages.create(
        body=message,
        from_=os.environ["TWILIO_FROM_NUMBER"],
        to=os.environ["ALERT_TO_NUMBER"],
    )
    return {"status": "sent", "sid": sent.sid}
