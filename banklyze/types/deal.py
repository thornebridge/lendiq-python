"""Deal response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from banklyze.types.common import PaginationMeta


# ── Summary sub-schemas ────────────────────────────────────────────────────


class BusinessSummary(BaseModel):
    business_name: str | None = None
    dba_name: str | None = None
    ein: str | None = None
    entity_type: str | None = None
    industry: str | None = None
    business_start_date: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    phone: str | None = None

    model_config = {"extra": "allow"}


class CoverageSummary(BaseModel):
    total_days_covered: int | None = None
    statement_period: str | None = None
    document_count: int | None = None
    document_types: list[str] | None = None

    model_config = {"extra": "allow"}


class FinancialsSummary(BaseModel):
    avg_monthly_deposits: float | None = None
    true_avg_monthly_deposits: float | None = None
    avg_daily_balance: float | None = None
    min_daily_balance: float | None = None
    max_daily_balance: float | None = None
    total_deposits: float | None = None
    total_withdrawals: float | None = None
    monthly_revenue_trend: str | None = None
    deposit_count: int | None = None
    negative_balance_days: int | None = None

    model_config = {"extra": "allow"}


class NsfOdSummary(BaseModel):
    nsf_fee_count: int | None = None
    nsf_fee_total: float | None = None
    overdraft_fee_count: int | None = None
    overdraft_fee_total: float | None = None

    model_config = {"extra": "allow"}


class ScreeningSummary(BaseModel):
    suspicious_count: int | None = None
    repeat_charges_count: int | None = None
    large_strange_count: int | None = None
    suspicious_items: list[dict] | None = None
    repeat_charges: list[dict] | None = None
    large_strange_items: list[dict] | None = None

    model_config = {"extra": "allow"}


class LargeDeposit(BaseModel):
    date: str | None = None
    amount: float | None = None
    description: str | None = None
    reasons: list[str] | None = None

    model_config = {"extra": "allow"}


class HealthSummary(BaseModel):
    """Health score summary with sub-factor breakdown.

    The ``factors`` dict contains up to 12 sub-factors, each with ``score``,
    ``max``, ``weight``, and ``detail`` keys.  Seven core sub-factors are always
    present (revenue, adb_stability, nsf_cleanliness, negative_days,
    deposit_consistency, screening_flags, deposit_quality).  Five optional
    sub-factors (revenue_trend, stacking, volatility, debt_service, eom_trend)
    appear when pipeline data is available.  Weights are normalized over the
    sub-factors present so the score is always 0–100.
    """

    health_score: float | None = None
    health_grade: str | None = None
    factors: dict | None = None

    model_config = {"extra": "allow"}


class RecommendationSummary(BaseModel):
    decision: str | None = None
    weighted_score: float | None = None
    confidence: float | None = None
    confidence_label: str | None = None
    risk_tier: str | None = None
    paper_grade: str | None = None
    paper_grade_detail: str | None = None
    advance_amount: float | None = None
    factor_rate: float | None = None
    holdback_pct: float | None = None
    est_daily_payment: float | None = None
    est_term_months: float | None = None
    funding_likelihood: str | None = None
    risk_factors: list[str] | None = None
    strengths: list[str] | None = None

    model_config = {"extra": "allow"}


class OwnerSummary(BaseModel):
    name: str | None = None
    title: str | None = None
    phone: str | None = None
    email: str | None = None
    ownership_pct: float | None = None
    credit_score: int | None = None
    address_street: str | None = None
    address_city: str | None = None
    address_state: str | None = None
    address_zip: str | None = None
    dob: str | None = None
    ssn_last4: str | None = None

    model_config = {"extra": "allow"}


class SelfReportedSummary(BaseModel):
    use_of_funds: str | None = None
    monthly_revenue: float | None = None
    annual_revenue: float | None = None
    monthly_credit_card_volume: float | None = None
    monthly_rent: float | None = None

    model_config = {"extra": "allow"}


class ExistingDebtSummary(BaseModel):
    mca_positions: int | None = None
    mca_balance: float | None = None
    lender_names: str | None = None
    has_term_loan: bool | None = None
    monthly_loan_payments: float | None = None
    has_tax_lien: bool | None = None
    has_judgment: bool | None = None
    has_bankruptcy: bool | None = None

    model_config = {"extra": "allow"}


class SourceSummary(BaseModel):
    source_type: str | None = None
    broker_name: str | None = None
    broker_company: str | None = None
    broker_email: str | None = None
    broker_phone: str | None = None
    commission_pct: float | None = None
    referral_source: str | None = None

    model_config = {"extra": "allow"}


class McaSummary(BaseModel):
    """MCA position and cash-flow analysis.

    ``mca_credit_score`` is the Layer 1 composite score derived solely from bank
    statement data.  It is **not** a bureau credit score.
    """

    positions_detected: int | None = None
    total_daily_obligation: float | None = None
    est_remaining_balance: float | None = None
    cash_flow_volatility_score: float | None = None
    daily_deposit_cv: float | None = None
    revenue_quality_score: float | None = None
    propping_risk: float | None = None
    avg_daily_deposit: float | None = None
    deposit_days_pct: float | None = None
    mca_credit_score: float | None = None
    credit_grade: str | None = None

    model_config = {"extra": "allow"}


class TaxReturnDealSummary(BaseModel):
    gross_receipts: float | None = None
    net_income: float | None = None
    form_type: str | None = None
    filing_year: int | None = None

    model_config = {"extra": "allow"}


class PnLDealSummary(BaseModel):
    revenue: float | None = None
    net_income: float | None = None
    net_margin: float | None = None
    period_start: str | None = None
    period_end: str | None = None

    model_config = {"extra": "allow"}


class CrossDocDealSummary(BaseModel):
    flags: list[dict] | None = None
    flag_count: int | None = None
    document_types: list[str] | None = None

    model_config = {"extra": "allow"}


# ── Top-level deal types ───────────────────────────────────────────────────


class DealSummary(BaseModel):
    """Summary deal object returned in list responses."""

    id: int
    business_name: str
    dba_name: str | None = None
    owner_name: str | None = None
    industry: str | None = None
    entity_type: str | None = None
    source_type: str | None = None
    status: str
    document_count: int = 0
    health_score: float | None = None
    health_grade: str | None = None
    avg_monthly_deposits: float | None = None
    avg_daily_balance: float | None = None
    funding_amount_requested: float | None = None
    screening_flags: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "allow"}


class DealDetail(BaseModel):
    """Full deal detail with all analysis sections."""

    report_date: str
    business: BusinessSummary
    funding_amount_requested: float | None = None
    ai_summary: str | None = None
    owner: OwnerSummary | None = None
    self_reported: SelfReportedSummary | None = None
    existing_debt: ExistingDebtSummary | None = None
    source: SourceSummary | None = None
    coverage: CoverageSummary
    financials: FinancialsSummary
    nsf_overdraft: NsfOdSummary
    screening: ScreeningSummary
    large_deposits: list[LargeDeposit] | None = None
    health: HealthSummary
    recommendation: RecommendationSummary | None = None
    mca: McaSummary | None = None
    tax_return: TaxReturnDealSummary | None = None
    pnl: PnLDealSummary | None = None
    cross_doc: CrossDocDealSummary | None = None
    processing_progress: float | None = None
    processing_stage: str | None = None

    model_config = {"extra": "allow"}


class DealListResponse(BaseModel):
    """Paginated list of deals."""

    data: list[DealSummary]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class DealNote(BaseModel):
    """A note attached to a deal."""

    id: int
    deal_id: int
    author: str
    content: str
    note_type: str | None = None
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class DealNotesListResponse(BaseModel):
    """Paginated list of deal notes."""

    data: list[DealNote]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class DealStats(BaseModel):
    """Aggregate deal statistics."""

    total: int
    by_status: dict[str, int]
    total_volume: float | None = None
    avg_health: float | None = None
    has_processing: bool = False

    model_config = {"extra": "allow"}


class DailyStatEntry(BaseModel):
    date: str
    total: int
    approved: int = 0
    declined: int = 0
    funded: int = 0
    avg_score: float | None = None

    model_config = {"extra": "allow"}


class DailyStatsResponse(BaseModel):
    period_days: int
    data: list[DailyStatEntry]

    model_config = {"extra": "allow"}
