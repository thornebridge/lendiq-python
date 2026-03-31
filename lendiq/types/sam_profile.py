"""SAM Search Profile response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from lendiq.types.common import PaginationMeta


class SAMProfileWatcher(BaseModel):
    """Watcher on a SAM search profile."""

    user_id: int
    display_name: str | None = None
    email: str | None = None
    notify_email: bool
    notify_in_app: bool
    attach_csv: bool

    model_config = {"extra": "allow"}


class SAMSearchProfile(BaseModel):
    """SAM search profile detail."""

    id: int
    name: str
    description: str | None = None
    naics_codes: list[str]
    state_codes: list[str]
    sba_business_types: list[str]
    min_suitability_score: int
    auto_create_deals: bool
    status: str
    schedule_interval: str | None = None
    schedule_day_of_week: int | None = None
    schedule_hour_utc: int
    next_run_at: datetime | None = None
    last_run_at: datetime | None = None
    last_run_id: int | None = None
    watchers: list[SAMProfileWatcher] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = {"extra": "allow"}


class SAMSearchProfileListResponse(BaseModel):
    """Paginated list of SAM search profiles."""

    data: list[SAMSearchProfile]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class SAMFetchRun(BaseModel):
    """SAM fetch run status."""

    id: int
    status: str
    search_criteria: dict = {}
    total_fetched: int = 0
    total_scored: int = 0
    total_qualified: int = 0
    total_deals_created: int = 0
    total_duplicates_skipped: int = 0
    total_disqualified: int = 0
    progress_pct: float = 0.0
    sam_total_records: int = 0
    created_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = {"extra": "allow"}


class SAMFetchRunListResponse(BaseModel):
    """Paginated list of SAM fetch runs."""

    data: list[SAMFetchRun]
    meta: PaginationMeta

    model_config = {"extra": "allow"}
