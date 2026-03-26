"""Instant analysis response types."""

from __future__ import annotations

from pydantic import BaseModel


class MCAPosition(BaseModel):
    """Detected MCA payment position."""

    amount: float
    count: int
    frequency: str
    description_pattern: str
    lender_name: str | None = None
    lender_type: str | None = None
    position_type: str | None = None
    regularity_score: float = 0
    daily_obligation: float = 0

    model_config = {"extra": "allow"}


class LargeDeposit(BaseModel):
    """Large deposit flagged during analysis."""

    date: str
    amount: float
    description: str
    reasons: list[str] = []

    model_config = {"extra": "allow"}


class ExpenseCategory(BaseModel):
    """Expense breakdown by category."""

    total: float
    count: int
    pct_of_expenses: float

    model_config = {"extra": "allow"}


class PositionCompliance(BaseModel):
    """MCA position payment compliance."""

    lender: str
    frequency: str
    expected_payments: int
    actual_payments: int
    missed_payments: int
    miss_rate: float

    model_config = {"extra": "allow"}


class InstantFileResult(BaseModel):
    """Analysis result for a single uploaded file."""

    filename: str
    status: str
    processing_ms: int = 0
    error: str | None = None

    bank_name: str | None = None
    account_last4: str | None = None
    account_type: str | None = None

    statement_start: str | None = None
    statement_end: str | None = None

    opening_balance: float | None = None
    closing_balance: float | None = None
    average_daily_balance: float | None = None
    min_daily_balance: float | None = None
    max_daily_balance: float | None = None
    negative_balance_days: int = 0

    transaction_count: int = 0
    deposit_count: int = 0
    withdrawal_count: int = 0
    total_deposits: float = 0
    total_withdrawals: float = 0

    nsf_count: int = 0
    overdraft_count: int = 0

    mca_positions: list[MCAPosition] = []
    mca_position_count: int = 0
    mca_daily_obligation: float = 0

    payment_processors: list[str] = []
    has_card_processing: bool = False

    deposit_types: dict[str, int] = {}
    primary_deposit_type: str | None = None
    cash_deposit_pct: float = 0

    ach_return_count: int = 0
    ach_return_critical_count: int = 0

    large_deposits: list[LargeDeposit] = []

    revenue_quality_score: float | None = None
    propping_risk: str | None = None
    round_trip_count: int = 0

    deposit_days_pct: float | None = None
    zero_deposit_days: int = 0

    cash_flow_volatility_score: float | None = None

    confidence: float = 0.0

    # Expense breakdown
    total_expenses: float = 0
    expense_count: int = 0
    expense_categories: dict[str, ExpenseCategory] = {}
    net_operating_income: float | None = None

    # Concentration
    concentration_risk: str | None = None
    top_source_pct_volume: float = 0
    unique_deposit_sources: int = 0

    # Liquidity
    days_of_cash: float | None = None
    liquidity_risk: str | None = None

    # Free cash flow
    daily_free_cash_flow: float | None = None
    monthly_free_cash_flow: float | None = None
    fcf_margin_pct: float | None = None
    fcf_risk: str | None = None

    # Trends
    net_trend_direction: str | None = None
    nsf_trend_direction: str | None = None

    model_config = {"extra": "allow"}


class InstantSummary(BaseModel):
    """Aggregate summary across all analyzed files."""

    total_files: int = 0
    successful: int = 0
    failed: int = 0

    total_deposits: float = 0
    total_withdrawals: float = 0
    avg_monthly_deposits: float = 0
    net_cash_flow: float = 0

    total_nsf: int = 0
    total_overdraft: int = 0
    total_ach_returns: int = 0

    total_mca_positions: int = 0
    total_mca_daily_obligation: float = 0

    payment_processors_found: list[str] = []
    has_card_processing: bool = False
    total_large_deposits: int = 0

    avg_revenue_quality: float | None = None
    any_propping_risk: bool = False

    date_range_start: str | None = None
    date_range_end: str | None = None
    months_covered: float = 0

    avg_days_of_cash: float | None = None
    worst_liquidity_risk: str | None = None
    avg_monthly_fcf: float | None = None

    net_trend_direction: str | None = None
    nsf_trend_direction: str | None = None

    model_config = {"extra": "allow"}


class InstantAnalysisResponse(BaseModel):
    """Response from the instant analysis endpoint."""

    session_id: str
    results: list[InstantFileResult]
    summary: InstantSummary

    model_config = {"extra": "allow"}


class FeedbackResponse(BaseModel):
    """Response from the instant analysis feedback endpoint."""

    status: str = "ok"

    model_config = {"extra": "allow"}
