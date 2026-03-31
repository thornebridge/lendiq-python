"""Usage metering response types."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel


class DocumentTypeUsage(BaseModel):
    """Usage breakdown for a single document type."""

    count: int = 0
    cost_usd: float = 0
    avg_processing_time_ms: int = 0

    model_config = {"extra": "allow"}


class ProcessingTimePercentiles(BaseModel):
    """Processing time percentiles for a document type."""

    p50_ms: int = 0
    p95_ms: int = 0
    p99_ms: int = 0

    model_config = {"extra": "allow"}


class ProcessingTimeStats(BaseModel):
    """Processing time percentiles with per-document-type breakdown."""

    p50_ms: int = 0
    p95_ms: int = 0
    p99_ms: int = 0
    by_document_type: dict[str, ProcessingTimePercentiles] = {}

    model_config = {"extra": "allow"}


class DailyUsage(BaseModel):
    """Usage for a single day."""

    date: date
    documents: int = 0
    cost_usd: float = 0

    model_config = {"extra": "allow"}


class UsageSummary(BaseModel):
    """Enhanced usage summary for an organization."""

    period_start: datetime
    total_documents: int = 0
    total_cost_usd: float = 0
    documents_this_month: int = 0
    cost_this_month: float = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    event_counts: dict[str, int] = {}
    budget_usd: int | None = None
    budget_remaining_usd: float | None = None
    by_document_type: dict[str, DocumentTypeUsage] = {}
    processing_times: ProcessingTimeStats = ProcessingTimeStats()
    daily_usage: list[DailyUsage] = []
    cost_by_type: dict[str, float] = {}

    model_config = {"extra": "allow"}
