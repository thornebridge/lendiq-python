"""Document triage response types."""

from __future__ import annotations

from pydantic import BaseModel


class TriagePageAnalysis(BaseModel):
    """Per-page analysis results."""

    page_number: int
    text_length: int
    has_transactions: bool = False
    has_dates: bool = False
    has_amounts: bool = False
    has_balance_keywords: bool = False
    classification: str = "other"
    relevance_score: float = 0.0

    model_config = {"extra": "allow"}


class DocumentClassification(BaseModel):
    """Classification result for the uploaded document."""

    document_type: str
    confidence: float = 0.0
    method: str = "heuristic"
    bank_name: str | None = None
    account_type: str | None = None
    account_last4: str | None = None

    model_config = {"extra": "allow"}


class QualityAssessment(BaseModel):
    """Overall quality assessment of the document."""

    text_quality_score: float = 0.0
    extraction_confidence: float = 0.0
    confidence_tier: str = "LOW"
    is_scanned: bool = False
    has_text_layer: bool = True
    avg_chars_per_page: float = 0.0
    issues: list[str] = []

    model_config = {"extra": "allow"}


class ConcatenationSignal(BaseModel):
    """Signals indicating multiple documents concatenated in one PDF."""

    is_likely_concatenated: bool = False
    confidence: float = 0.0
    signals: list[str] = []
    estimated_document_count: int = 1
    boundary_pages: list[int] = []

    model_config = {"extra": "allow"}


class TransactionSignals(BaseModel):
    """Early transaction-level signals from regex prescreen."""

    estimated_count: int = 0
    deposit_count: int = 0
    withdrawal_count: int = 0
    nsf_count: int = 0
    overdraft_count: int = 0
    detected_sections: list[str] = []
    sign_convention: str = "unknown"
    has_running_balance: bool = False

    model_config = {"extra": "allow"}


class IntegrityCheck(BaseModel):
    """PDF metadata and structural integrity checks."""

    risk_level: str = "clean"
    flags: list[str] = []
    font_families_detected: int | None = None
    page_dimension_groups: int = 1

    model_config = {"extra": "allow"}


class TriageRecommendation(BaseModel):
    """Overall recommendation for the document."""

    action: str
    reasons: list[str] = []

    model_config = {"extra": "allow"}


class TriageResponse(BaseModel):
    """Full triage response for a single PDF."""

    filename: str
    page_count: int
    processing_ms: int

    classification: DocumentClassification
    quality: QualityAssessment
    pages: list[TriagePageAnalysis]
    concatenation: ConcatenationSignal
    transaction_signals: TransactionSignals
    integrity: IntegrityCheck
    recommendation: TriageRecommendation

    model_config = {"extra": "allow"}
