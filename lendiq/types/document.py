"""Document and transaction response types."""

from __future__ import annotations

import warnings
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

from lendiq.types.common import HealthFactor, PaginationMeta, ValidationDiscrepancy

# ---------------------------------------------------------------------------
# Literal type aliases
# ---------------------------------------------------------------------------

DocumentType = Literal[
    "bank_statement", "tax_return", "profit_and_loss",
    "drivers_license", "voided_check", "other",
]

ProcessingStatus = Literal[
    "uploaded", "classifying", "extracting", "computing_metrics",
    "screening", "scoring", "completed", "failed", "cancelled",
]

ExtractionMethod = Literal[
    "gemini_native_pdf", "pdfplumber", "paddle_ocr", "surya",
    "tesseract", "textract", "llm_vision", "claude_native_pdf", "hybrid",
]

# ---------------------------------------------------------------------------
# Deprecated models — kept for backward compatibility
# ---------------------------------------------------------------------------


class PrescreenSummary(BaseModel):
    """Pre-screen results from regex extraction (no LLM).

    .. deprecated::
        This model is deprecated and will be removed in a future release.
    """

    bank_name: str | None = None
    account_last4: str | None = None
    opening_balance: Decimal | None = None
    closing_balance: Decimal | None = None
    start_date: date | None = None
    end_date: date | None = None
    est_transaction_count: int | None = None
    text_quality: float | None = None
    viable: bool | None = None
    rejection_reasons: list[str] | None = None
    confidence: float | None = None
    completed_at: datetime | None = None

    model_config = {"extra": "allow"}

    def __init_subclass__(cls, **kwargs: object) -> None:
        warnings.warn(
            "PrescreenSummary is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init_subclass__(**kwargs)


class FieldConfidence(BaseModel):
    """Confidence for a single extracted field."""

    field_name: str
    value: str | None = None
    confidence: str = "medium"
    confidence_score: float = 0.0
    source: str | None = None
    discrepancy: bool = False

    model_config = {"extra": "allow"}


class ExtractionConfidenceDetail(BaseModel):
    """Complete extraction confidence breakdown.

    .. deprecated::
        This model is deprecated and will be removed in a future release.
    """

    overall_confidence: float = 0.0
    overall_tier: str = "medium"
    fields: list[FieldConfidence] = []
    high_confidence_count: int = 0
    low_confidence_count: int = 0
    fields_requiring_review: list[str] = []

    model_config = {"extra": "allow"}

    def __init_subclass__(cls, **kwargs: object) -> None:
        warnings.warn(
            "ExtractionConfidenceDetail is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init_subclass__(**kwargs)


class DriverLicenseAnalysis(BaseModel):
    """Analysis results for a driver's license document."""

    full_name: str | None = None
    date_of_birth: str | None = None
    license_number_last4: str | None = None
    address_street: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    expiration_date: str | None = None
    state_of_issuance: str | None = None
    photo_readable: bool | None = None
    extraction_confidence: float | None = None
    notes: str | None = None
    model_config = {"extra": "allow"}


class VoidedCheckAnalysis(BaseModel):
    """Analysis results for a voided check document."""

    bank_name: str | None = None
    routing_number: str | None = None
    account_number_last4: str | None = None
    account_holder_name: str | None = None
    check_number: str | None = None
    bank_address: str | None = None
    is_voided: bool | None = None
    micr_readable: bool | None = None
    extraction_confidence: float | None = None
    notes: str | None = None
    model_config = {"extra": "allow"}


class DocumentIntegrity(BaseModel):
    """Document integrity / tampering detection summary."""

    tampering_risk_level: str
    tampering_flags: list[str] = []
    font_families_detected: int | None = None

    model_config = {"extra": "allow"}


class DocumentSummary(BaseModel):
    """Document summary in list responses."""

    id: int
    filename: str
    document_type: DocumentType = "bank_statement"
    bank_name: str | None = None
    account_holder_name: str | None = None
    statement_start_date: date | None = None
    statement_end_date: date | None = None
    status: str
    health_grade: str | None = None
    pdf_risk_level: str | None = None
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class AnalysisSummary(BaseModel):
    """Bank statement analysis results."""

    average_daily_balance: Decimal | None = None
    min_daily_balance: Decimal | None = None
    max_daily_balance: Decimal | None = None
    negative_balance_days: int = 0
    total_deposits: Decimal | None = None
    deposit_count: int = 0
    average_deposit_amount: Decimal | None = None
    average_monthly_deposits: Decimal | None = None
    total_withdrawals: Decimal | None = None
    withdrawal_count: int = 0
    large_deposit_count: int = 0
    large_deposit_total: Decimal | None = None
    nsf_fee_count: int = 0
    nsf_fee_total: Decimal | None = None
    overdraft_fee_count: int = 0
    overdraft_fee_total: Decimal | None = None
    large_strange_count: int = 0
    repeat_charges_count: int = 0
    suspicious_count: int = 0
    ai_screening_used: bool = False
    health_score: Decimal | None = None
    health_grade: str | None = None
    true_deposits: Decimal | None = None
    true_average_monthly_deposits: Decimal | None = None
    non_operating_pct: float | None = None
    validation_is_reliable: bool | None = None
    validation_discrepancies: list[ValidationDiscrepancy] | None = None
    health_factors_json: dict[str, HealthFactor] | None = None
    deposit_mix: dict | None = None

    model_config = {"extra": "allow"}


class DocumentDetail(BaseModel):
    """Full document detail including analysis."""

    id: int
    filename: str
    document_type: DocumentType = "bank_statement"
    classification_confidence: float | None = None
    bank_name: str | None = None
    account_number_last4: str | None = None
    account_holder_name: str | None = None
    statement_start_date: date | None = None
    statement_end_date: date | None = None
    opening_balance: Decimal | None = None
    closing_balance: Decimal | None = None
    status: str
    extraction_method: ExtractionMethod | None = None
    extraction_confidence: float | None = None
    confidence_tier: str | None = None
    pdf_risk_level: str | None = None
    file_size_bytes: int | None = None
    page_count: int | None = None
    processing_started_at: datetime | None = None
    processing_completed_at: datetime | None = None
    processing_cost_usd: float | None = None
    error_message: str | None = None
    health_grade: str | None = None
    deal_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    gemini_model_override: str | None = None
    analysis: AnalysisSummary | None = None
    pdf_url: str | None = None
    tax_return_analysis: dict | None = None
    pnl_analysis: dict | None = None
    driver_license_analysis: DriverLicenseAnalysis | None = None
    voided_check_analysis: VoidedCheckAnalysis | None = None
    integrity: DocumentIntegrity | None = None

    model_config = {"extra": "allow"}


class DocumentUploadResponse(BaseModel):
    """Response from document upload."""

    id: int
    filename: str
    status: str
    message: str

    model_config = {"extra": "allow"}


class DocumentStatusResponse(BaseModel):
    """Lightweight document processing status."""

    id: int
    status: str
    document_type: DocumentType = "bank_statement"
    error_message: str | None = None
    processing_started_at: datetime | None = None
    processing_completed_at: datetime | None = None

    model_config = {"extra": "allow"}


class DocumentListResponse(BaseModel):
    """Paginated list of documents."""

    data: list[DocumentSummary]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class BulkUploadItemResponse(BaseModel):
    filename: str
    status: str
    document_id: int | None = None
    error: str | None = None

    model_config = {"extra": "allow"}


class BulkUploadResponse(BaseModel):
    """Response from bulk document upload."""

    total: int
    queued: int
    failed: int
    results: list[BulkUploadItemResponse]

    model_config = {"extra": "allow"}


class BatchDocumentStatusItem(BaseModel):
    """Status of a single document in a batch status check."""

    id: int
    filename: str | None = None
    status: str
    bank_name: str | None = None
    error_message: str | None = None
    processing_cost_usd: float | None = None
    created_at: str | None = None

    model_config = {"extra": "allow"}


class BatchDocumentStatusResponse(BaseModel):
    """Response from batch document status check."""

    documents: dict[str, BatchDocumentStatusItem]

    model_config = {"extra": "allow"}
