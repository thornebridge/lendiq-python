"""CRM integration response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from banklyze.types.common import PaginationMeta


class CRMConfigResponse(BaseModel):
    """CRM configuration for a provider."""

    provider: str
    enabled: bool = False
    api_url: str | None = None
    last_sync_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "allow"}


class ConnectionTestResponse(BaseModel):
    """Result of testing a CRM connection."""

    success: bool
    message: str | None = None
    provider: str | None = None

    model_config = {"extra": "allow"}


class FieldMappingResponse(BaseModel):
    """Field mapping configuration for a CRM provider."""

    provider: str
    mappings: dict[str, str] = {}
    custom_fields: dict[str, str] = {}

    model_config = {"extra": "allow"}


class SyncTriggerResponse(BaseModel):
    """Response from triggering a CRM sync."""

    status: str
    message: str | None = None
    deal_id: int | None = None

    model_config = {"extra": "allow"}


class SyncLogEntry(BaseModel):
    """A single CRM sync log entry."""

    id: int
    provider: str
    deal_id: int | None = None
    direction: str | None = None
    status: str
    error: str | None = None
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class SyncLogResponse(BaseModel):
    """Paginated CRM sync log."""

    data: list[SyncLogEntry]
    meta: PaginationMeta

    model_config = {"extra": "allow"}
