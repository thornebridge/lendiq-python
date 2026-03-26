"""BVL (Banklyze Validation Layer) response types."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from banklyze.types.common import PaginationMeta


class BVLSignal(BaseModel):
    """Individual validation signal within a factor group."""

    name: str
    value: Any = None
    score: float
    confidence: float
    detail: str
    source: str

    model_config = {"extra": "allow"}


class BVLHardGate(BaseModel):
    """Hard gate failure that triggers disqualification."""

    gate_name: str
    detail: str
    source: str

    model_config = {"extra": "allow"}


class BVLResult(BaseModel):
    """Validation result for a single deal."""

    deal_id: int
    lead_score: float | None = None
    lead_grade: str | None = None
    score_tier: str | None = None
    highest_tier_completed: str | None = None
    disqualified: bool = False
    disqualification_reason: str | None = None
    factors: dict[str, Any] | None = None
    hard_gates: list[BVLHardGate] | None = None
    signals_financial: list[BVLSignal] | None = None
    signals_business: list[BVLSignal] | None = None
    signals_contact: list[BVLSignal] | None = None
    signals_compliance: list[BVLSignal] | None = None
    signals_web: list[BVLSignal] | None = None
    signals_geographic: list[BVLSignal] | None = None
    signals_industry: list[BVLSignal] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "allow"}


class BVLRun(BaseModel):
    """Batch validation run status."""

    id: int
    status: str
    current_tier: str | None = None
    total_leads: int
    processed_leads: int = 0
    promoted_tier2: int = 0
    promoted_tier3: int = 0
    disqualified_leads: int = 0
    progress_pct: float = 0.0
    queue_position: int | None = None
    estimated_completion: datetime | None = None
    filter_status: str | None = None
    max_tier: str | None = None
    callback_url: str | None = None
    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = {"extra": "allow"}


class BVLRunListResponse(BaseModel):
    """Paginated list of BVL runs."""

    data: list[BVLRun]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class CallQueueLead(BaseModel):
    """Lead entry in the prioritized call queue."""

    deal_id: int
    business_name: str
    lead_score: float | None = None
    lead_grade: str | None = None
    score_tier: str | None = None
    business_phone: str | None = None
    business_email: str | None = None
    owner_name: str | None = None
    industry: str | None = None
    state: str | None = None
    funding_amount_requested: float | None = None
    last_validated_at: datetime | None = None

    model_config = {"extra": "allow"}


class CallQueueResponse(BaseModel):
    """Paginated call queue response."""

    data: list[CallQueueLead]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class BVLStats(BaseModel):
    """Org-level BVL validation statistics."""

    total_validated: int = 0
    total_disqualified: int = 0
    by_tier: dict[str, int] = {}
    avg_score: float | None = None
    grade_distribution: dict[str, int] = {}
    top_disqualification_reasons: list[str] = []

    model_config = {"extra": "allow"}


# ── SAM entity types ────────────────────────────────────────────────────────


class SAMEntity(BaseModel):
    """SAM.gov entity record."""

    id: int
    uei: str | None = None
    legal_business_name: str | None = None
    dba_name: str | None = None
    cage_code: str | None = None
    entity_status: str | None = None
    physical_address_city: str | None = None
    physical_address_state: str | None = None
    naics_codes: list[str] = []
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class SAMEntityListResponse(BaseModel):
    """Paginated list of SAM entities."""

    data: list[SAMEntity]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class SAMStatsResponse(BaseModel):
    """SAM entity fetch statistics."""

    total_entities: int = 0
    total_runs: int = 0
    by_status: dict[str, int] = {}

    model_config = {"extra": "allow"}
