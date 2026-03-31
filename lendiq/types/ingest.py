"""Ingest and batch response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class IngestDocumentResult(BaseModel):
    """Status of a single file in an ingest request."""

    filename: str
    document_id: int | None = None
    status: str
    document_type: str | None = None
    error: str | None = None

    model_config = {"extra": "allow"}


class IngestResponse(BaseModel):
    """Response from a bulk ingest request."""

    batch_id: int
    deal_id: int
    deal_created: bool
    external_reference: str | None = None
    total: int
    queued: int
    failed: int
    results: list[IngestDocumentResult]

    model_config = {"extra": "allow"}


class BatchDocumentStatus(BaseModel):
    document_id: int
    filename: str | None = None
    document_type: str | None = None
    status: str
    error_message: str | None = None

    model_config = {"extra": "allow"}


class BatchRecommendationSummary(BaseModel):
    decision: str
    weighted_score: float
    risk_tier: str
    paper_grade: str

    model_config = {"extra": "allow"}


class BatchStatusResponse(BaseModel):
    """Status of a processing batch."""

    batch_id: int
    deal_id: int
    status: str
    total_documents: int
    completed_documents: int
    failed_documents: int
    created_at: datetime
    completed_at: datetime | None = None
    documents: list[BatchDocumentStatus]
    recommendation: BatchRecommendationSummary | None = None

    model_config = {"extra": "allow"}
