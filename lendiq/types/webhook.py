"""Webhook response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class WebhookConfig(BaseModel):
    """Webhook configuration."""

    url: str | None = None
    events: list[str] = []
    enabled: bool = True
    has_secret: bool = False

    model_config = {"extra": "allow"}


class WebhookTestResult(BaseModel):
    """Result of a webhook test delivery."""

    delivered: bool
    status_code: int | None = None
    error: str | None = None

    model_config = {"extra": "allow"}


class WebhookDelivery(BaseModel):
    """A webhook delivery log entry."""

    id: int
    event_type: str
    event_id: str
    url: str | None = None
    status_code: int | None = None
    latency_ms: int | None = None
    attempt: int = 1
    max_attempts: int = 3
    success: bool = False
    error_message: str | None = None
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class WebhookDeliveryDetail(WebhookDelivery):
    """Extended delivery detail with payload and response body."""

    payload_json: str | None = None
    response_body: str | None = None


class WebhookDeliveryListResponse(BaseModel):
    """Paginated list of webhook deliveries."""

    data: list[WebhookDelivery]
    meta: PaginationMeta

    model_config = {"extra": "allow"}
