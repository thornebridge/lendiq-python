"""Collaboration response types — assignments, comments, doc requests, timeline, user search."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


# ── Assignment types ────────────────────────────────────────────────────────


class Assignment(BaseModel):
    """A user assignment on a deal."""

    id: int
    deal_id: int
    user_id: int
    role: str
    assigned_by_id: int | None = None
    created_at: datetime | None = None
    user_email: str | None = None
    user_display_name: str | None = None

    model_config = {"extra": "allow"}


class AssignmentListResponse(BaseModel):
    """List of deal assignments."""

    data: list[Assignment]

    model_config = {"extra": "allow"}


# ── Comment types ───────────────────────────────────────────────────────────


class Comment(BaseModel):
    """A comment on a deal."""

    id: int
    deal_id: int
    author_id: int
    parent_id: int | None = None
    content: str
    mentions: list[int] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    author_email: str | None = None
    author_display_name: str | None = None

    model_config = {"extra": "allow"}


class CommentListResponse(BaseModel):
    """List of deal comments."""

    data: list[Comment]

    model_config = {"extra": "allow"}


# ── Document Request types ──────────────────────────────────────────────────


class DocRequest(BaseModel):
    """A document request on a deal."""

    id: int
    deal_id: int
    document_type: str
    description: str | None = None
    recipient_email: str | None = None
    status: str
    due_date: date | None = None
    fulfilled_at: datetime | None = None
    document_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "allow"}


class DocRequestListResponse(BaseModel):
    """List of document requests."""

    data: list[DocRequest]

    model_config = {"extra": "allow"}


# ── Activity Timeline types ────────────────────────────────────────────────


class ActivityEvent(BaseModel):
    """An activity event in the timeline."""

    id: int
    event_type: str
    summary: str
    actor_name: str | None = None
    actor_id: int | None = None
    deal_id: int | None = None
    metadata: dict | None = None
    created_at: datetime | None = None

    model_config = {"extra": "allow"}


class TimelineResponse(BaseModel):
    """Paginated activity timeline."""

    data: list[ActivityEvent]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


# ── User Search types ──────────────────────────────────────────────────────


class UserSearchResult(BaseModel):
    """A user returned from search."""

    id: int
    email: str
    display_name: str | None = None
    role: str

    model_config = {"extra": "allow"}


class UserSearchResponse(BaseModel):
    """List of users matching a search query."""

    data: list[UserSearchResult]

    model_config = {"extra": "allow"}


# ── Assigned Deals types ──────────────────────────────────────────────────


class AssignedDealItem(BaseModel):
    """A deal assigned to the current user."""

    id: int
    business_name: str
    status: str
    health_grade: str | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "allow"}


class AssignedDealsResponse(BaseModel):
    """Paginated list of deals assigned to the current user."""

    data: list[AssignedDealItem]
    meta: PaginationMeta

    model_config = {"extra": "allow"}
