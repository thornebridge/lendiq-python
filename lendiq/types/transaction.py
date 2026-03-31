"""Transaction response types."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class Transaction(BaseModel):
    """A single bank transaction."""

    id: int
    date: date
    description: str
    amount: Decimal
    balance: Decimal | None = None
    transaction_type: str | None = None
    is_nsf_fee: bool = False
    is_overdraft_fee: bool = False
    is_large_deposit: bool = False
    is_large_strange: bool = False
    is_repeat_charge: bool = False
    is_suspicious: bool = False
    screening_bucket: str | None = None
    flag_reason: str | None = None
    is_corrected: bool = False
    correction_count: int = 0

    model_config = {"extra": "allow"}


class TransactionListResponse(BaseModel):
    """Paginated list of transactions."""

    data: list[Transaction]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class TransactionCorrection(BaseModel):
    """A correction applied to a transaction."""

    id: int
    field_name: str
    original_value: str
    corrected_value: str
    correction_reason: str
    corrected_by_name: str | None = None
    created_at: datetime

    model_config = {"extra": "allow"}


class TransactionCorrectionListResponse(BaseModel):
    """List of corrections for a transaction."""

    data: list[TransactionCorrection]

    model_config = {"extra": "allow"}


class TransactionDetail(BaseModel):
    """Full transaction detail returned after a correction."""

    id: int
    date: date
    description: str
    amount: Decimal
    balance: Decimal | None = None
    transaction_type: str | None = None
    is_nsf_fee: bool = False
    is_overdraft_fee: bool = False
    is_large_deposit: bool = False
    is_large_strange: bool = False
    is_repeat_charge: bool = False
    is_suspicious: bool = False
    screening_bucket: str | None = None
    flag_reason: str | None = None
    is_corrected: bool = False
    correction_count: int = 0

    model_config = {"extra": "allow"}
