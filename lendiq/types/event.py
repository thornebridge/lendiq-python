"""Server-Sent Event types."""

from __future__ import annotations

from pydantic import BaseModel


class SSEEvent(BaseModel):
    """A server-sent event from the LendIQ API."""

    event: str | None = None
    data: str | None = None
    id: str | None = None
    retry: int | None = None

    model_config = {"extra": "allow"}
