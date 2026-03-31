"""Dead letter queue response types."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class DlqEntry(BaseModel):
    """A single dead letter queue entry."""

    id: int
    task_name: str
    args_json: Any = None
    error_message: str | None = None
    attempts: int = 0
    status: str
    created_at: datetime | None = None
    resolved_at: datetime | None = None

    model_config = {"extra": "allow"}


class DlqListResponse(BaseModel):
    """Paginated list of dead letter queue entries."""

    data: list[DlqEntry]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class DlqActionResponse(BaseModel):
    """Response from a DLQ action (retry, discard)."""

    status: str
    id: int
    task_name: str | None = None

    model_config = {"extra": "allow"}
