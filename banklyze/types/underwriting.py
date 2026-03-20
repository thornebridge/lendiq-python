"""Underwriting recommendation response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Recommendation(BaseModel):
    """Full underwriting recommendation for a deal.

    For declined deals, ``hypothetical_cfcr`` and ``hypothetical_dscr`` contain
    the projected ratios if the advance *were* funded — useful for
    near-miss analysis.  ``mca_credit_score`` is the Layer 1 composite score
    derived solely from bank statement data.
    """

    id: int
    deal_id: int
    decision: str
    weighted_score: float
    risk_tier: str
    paper_grade: str | None = None
    paper_grade_detail: str | None = None
    advance_amount: float | None = None
    advance_range_low: float | None = None
    advance_range_high: float | None = None
    factor_rate: float | None = None
    holdback_pct: float | None = None
    est_daily_payment: float | None = None
    est_term_months: float | None = None
    funding_likelihood: str | None = None
    funding_likelihood_reason: str | None = None
    documents_analyzed: int | None = None
    cross_doc_flags: list | None = None
    cross_doc_flag_count: int | None = None
    risk_factors: list[str] = []
    strengths: list[str] = []
    hard_decline_reasons: list[str] = []
    criteria_scores: dict = {}
    confidence: float | None = None
    confidence_label: str | None = None
    stress_test_passed: bool | None = None
    layer_scores: dict = {}
    forecast: dict | None = None
    cash_flow_coverage_ratio: float | None = None
    dscr: float | None = None
    hypothetical_cfcr: float | None = None
    hypothetical_dscr: float | None = None
    mca_credit_score: float | None = None
    ruleset_id: int | None = None
    ruleset_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "allow"}
