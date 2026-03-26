"""Admin response types — error logs, usage summary, daily, and models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from banklyze.types.common import PaginationMeta


# ── Error log types ──────────────────────────────────────────────────────────


class ErrorLogEntry(BaseModel):
    """A single error log entry."""

    id: int
    severity: str | None = None
    source: str | None = None
    error_type: str | None = None
    message: str | None = None
    document_id: int | None = None
    deal_id: int | None = None
    request_path: str | None = None
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class ErrorLogListResponse(BaseModel):
    """Paginated list of error log entries."""

    data: list[ErrorLogEntry]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


# ── Usage summary types ──────────────────────────────────────────────────────


class UsageSummaryTotals(BaseModel):
    """Aggregate totals for a usage period."""

    total_calls: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0

    model_config = {"extra": "allow"}


class UsageSummaryByEvent(BaseModel):
    """Usage breakdown for a single event type."""

    event_type: str
    count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    avg_duration_ms: float = 0.0

    model_config = {"extra": "allow"}


class UsageSummaryByModel(BaseModel):
    """Usage breakdown for a single model."""

    model_name: str
    count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    avg_duration_ms: float = 0.0

    model_config = {"extra": "allow"}


class UsageSummaryResponse(BaseModel):
    """Full usage summary for a period."""

    period_days: int
    totals: UsageSummaryTotals
    by_event_type: list[UsageSummaryByEvent]
    by_model: list[UsageSummaryByModel]
    document_counts: dict[str, int]
    error_counts: dict[str, int]

    model_config = {"extra": "allow"}


# ── Usage daily types ────────────────────────────────────────────────────────


class UsageDailyEntry(BaseModel):
    """Usage for a single day."""

    day: str
    events: int = 0
    tokens: int = 0
    cost: float = 0.0

    model_config = {"extra": "allow"}


class UsageDailyResponse(BaseModel):
    """Daily usage breakdown."""

    days: list[UsageDailyEntry]

    model_config = {"extra": "allow"}


# ── Usage models types ───────────────────────────────────────────────────────


class UsageModelsEntry(BaseModel):
    """Usage breakdown for a single model."""

    model_name: str
    count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    avg_duration_ms: float = 0.0

    model_config = {"extra": "allow"}


class UsageModelsResponse(BaseModel):
    """Usage breakdown by model."""

    models: list[UsageModelsEntry]

    model_config = {"extra": "allow"}


# ── Health types ────────────────────────────────────────────────────────────


class HealthResponse(BaseModel):
    """System health status."""

    db_connected: bool
    pipeline_success_rate_24h: float
    pipelines_last_24h: int
    queue_depth: int

    model_config = {"extra": "allow"}
