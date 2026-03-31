"""Share link response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ShareToken(BaseModel):
    """A share token for public deal access."""

    id: int
    token: str
    share_url: str
    view_mode: str
    expires_at: datetime | None = None
    created_at: datetime

    model_config = {"extra": "allow"}


class ShareTokenListItem(BaseModel):
    """A share token with usage statistics."""

    id: int
    token: str
    share_url: str
    view_mode: str
    is_active: bool
    expires_at: datetime | None = None
    access_count: int = 0
    last_accessed_at: datetime | None = None
    created_at: datetime

    model_config = {"extra": "allow"}


class ShareTokenListResponse(BaseModel):
    """List of share tokens for a deal."""

    data: list[ShareTokenListItem]

    model_config = {"extra": "allow"}
