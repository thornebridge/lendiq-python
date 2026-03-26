"""Integration response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class WebhookHealth(BaseModel):
    """Webhook delivery health metrics."""

    delivery_rate_24h: float | None = None
    avg_latency_ms: float | None = None
    total_deliveries_24h: int = 0
    successful_deliveries_24h: int = 0
    failed_deliveries_24h: int = 0

    model_config = {"extra": "allow"}


class ApiHealth(BaseModel):
    """API error rate metrics."""

    error_rate_24h: float | None = None
    total_requests_24h: int = 0
    error_count_24h: int = 0

    model_config = {"extra": "allow"}


class QuotaUsage(BaseModel):
    """Document quota usage metrics."""

    documents_this_month: int = 0
    documents_limit: int | None = None
    documents_remaining: int | None = None
    usage_pct: float | None = None

    model_config = {"extra": "allow"}


class QueueHealth(BaseModel):
    """Queue depth and priority breakdown."""

    active_pipelines: int = 0
    queue_depth: int = 0
    by_priority: dict[str, int] = {}

    model_config = {"extra": "allow"}


class IntegrationHealthResponse(BaseModel):
    """Integration health dashboard — webhook delivery, API errors, quota, queue."""

    webhooks: WebhookHealth
    api: ApiHealth
    quota: QuotaUsage
    queue: QueueHealth

    model_config = {"extra": "allow"}


class Integration(BaseModel):
    """A configured integration for an organization."""

    integration_type: str
    enabled: bool = True
    label: str | None = None
    last_test_at: datetime | None = None
    last_test_success: bool | None = None
    last_test_error: str | None = None
    created_at: datetime | None = None
    has_credentials: bool = False

    model_config = {"extra": "allow"}


class IntegrationTestResponse(BaseModel):
    """Result of testing an integration."""

    success: bool
    message: str | None = None

    model_config = {"extra": "allow"}
