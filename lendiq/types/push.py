"""Push notification response types."""

from __future__ import annotations

from pydantic import BaseModel


class VapidKeyResponse(BaseModel):
    """VAPID public key for web push subscriptions."""

    public_key: str

    model_config = {"extra": "allow"}


class PushStatusResponse(BaseModel):
    """Status response for push subscription operations."""

    status: str
    message: str | None = None

    model_config = {"extra": "allow"}
