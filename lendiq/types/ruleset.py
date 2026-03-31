"""Ruleset response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class Ruleset(BaseModel):
    """An underwriting ruleset with thresholds and scoring weights."""

    id: int
    name: str
    description: str | None = None
    is_default: bool

    # Hard decline thresholds
    min_monthly_deposits: float
    min_days_covered: int
    min_health_score: float
    max_suspicious_count: int
    max_nsf_per_month: float
    max_debt_service_ratio: float

    # Scoring thresholds
    min_adb_pct_of_revenue: float
    min_deposit_frequency: int
    revenue_decline_red_flag_pct: float

    # Decision thresholds
    approve_min_score: float
    conditional_min_score: float

    # Paper grade thresholds
    grade_a_min_score: float
    grade_b_min_score: float
    grade_c_min_score: float

    # CFCR
    min_cfcr: float

    # Scoring weights
    weight_revenue: float
    weight_balance_health: float
    weight_nsf_overdraft: float
    weight_deposit_frequency: float
    weight_revenue_trend: float
    weight_debt_service: float
    weight_transaction_screening: float
    weight_health_score: float
    weight_cross_doc: float

    # MCA-specific scoring weights
    weight_position_stacking: float
    weight_cash_flow_volatility: float
    weight_revenue_quality: float
    weight_daily_velocity: float

    updated_at: datetime | None = None
    updated_by: str | None = None

    model_config = {"extra": "allow"}


class RulesetListResponse(BaseModel):
    """List of rulesets."""

    data: list[Ruleset]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class RulesetEvaluation(BaseModel):
    """Result of evaluating a deal against a ruleset."""

    ruleset_id: int | None = None
    ruleset_name: str
    decision: str
    weighted_score: float
    risk_tier: str
    paper_grade: str | None = None
    advance_amount: float | None = None
    advance_range_low: float | None = None
    advance_range_high: float | None = None
    factor_rate: float | None = None
    holdback_pct: float | None = None
    risk_factors: list[str] = []
    strengths: list[str] = []
    hard_decline_reasons: list[str] = []
    criteria_scores: dict = {}
    confidence: float | None = None
    confidence_label: str | None = None
    stress_test_passed: bool | None = None
    layer_scores: dict = {}
    forecast: dict | None = None

    model_config = {"extra": "allow"}


class ComparativeEvaluationResponse(BaseModel):
    """Comparative evaluation of a deal across multiple rulesets."""

    deal_id: int
    evaluations: list[RulesetEvaluation]
    best_fit: RulesetEvaluation | None = None

    model_config = {"extra": "allow"}
