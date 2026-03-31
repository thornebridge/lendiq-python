"""Review response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from lendiq.types.common import PaginationMeta


class ReviewListItem(BaseModel):
    id: int
    deal_id: int | None = None
    filename: str
    bank_name: str | None = None
    review_status: str
    health_score: float | None = None
    health_grade: str | None = None
    validation_is_reliable: bool | None = None
    transaction_count: int = 0
    total_deposits: float | None = None
    created_at: datetime

    model_config = {"extra": "allow"}


class ReviewListResponse(BaseModel):
    data: list[ReviewListItem]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class TransactionReviewItem(BaseModel):
    id: int
    date: str
    description: str
    amount: float
    balance: float | None = None
    transaction_type: str | None = None
    extraction_confidence: float | None = None
    is_nsf_fee: bool = False
    is_overdraft_fee: bool = False

    model_config = {"extra": "allow"}


class ReviewDetailResponse(BaseModel):
    id: int
    filename: str
    bank_name: str | None = None
    review_status: str
    opening_balance: float | None = None
    closing_balance: float | None = None
    statement_start_date: str | None = None
    statement_end_date: str | None = None
    health_score: float | None = None
    health_grade: str | None = None
    validation_is_reliable: bool | None = None
    extraction_audit: dict | None = None
    transactions: list[TransactionReviewItem] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ReviewActionResponse(BaseModel):
    id: int
    review_status: str
    message: str

    model_config = {"extra": "allow"}
