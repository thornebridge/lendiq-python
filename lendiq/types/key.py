"""API key response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class APIKey(BaseModel):
    """An API key (without the raw secret)."""

    id: int
    name: str
    key_prefix: str
    scopes: str
    expires_at: datetime | None = None
    last_used_at: datetime | None = None
    revoked_at: datetime | None = None
    is_active: bool = True
    created_at: datetime

    model_config = {"extra": "allow"}


class CreateKeyResponse(BaseModel):
    """Response from creating a new API key — includes the raw key (shown only once)."""

    id: int
    name: str
    key: str
    key_prefix: str
    scopes: str
    expires_at: datetime | None = None
    created_at: datetime | None = None
    message: str = "Store this key securely. It will not be shown again."

    model_config = {"extra": "allow"}


class KeyListResponse(BaseModel):
    """Paginated list of API keys."""

    data: list[APIKey]
    meta: PaginationMeta

    model_config = {"extra": "allow"}
