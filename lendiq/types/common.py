"""Common response types shared across all resources."""

from __future__ import annotations

from pydantic import BaseModel


class PaginationMeta(BaseModel):
    """Pagination metadata returned with list responses."""

    page: int
    per_page: int
    total: int
    total_pages: int

    model_config = {"extra": "allow"}


class ActionResponse(BaseModel):
    """Generic action confirmation response."""

    status: str
    message: str

    model_config = {"extra": "allow"}


class ErrorDetail(BaseModel):
    """Structured error response from the API."""

    error: str
    detail: str | None = None
    code: str | None = None

    model_config = {"extra": "allow"}


class HealthFactor(BaseModel):
    """Single health score sub-factor breakdown."""

    score: float
    max: float
    weight: float
    detail: str | None = None

    model_config = {"extra": "allow"}


class ValidationDiscrepancy(BaseModel):
    """Extraction validation discrepancy."""

    check_type: str
    severity: str
    detail: str
    expected: str | None = None
    actual: str | None = None

    model_config = {"extra": "allow"}
