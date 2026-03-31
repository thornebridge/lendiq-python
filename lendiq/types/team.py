"""Team management response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class TeamMember(BaseModel):
    """A team member within an organization."""

    id: int
    email: str
    display_name: str | None = None
    role: str
    is_active: bool
    status: str
    last_login_at: datetime | None = None
    created_at: datetime

    model_config = {"extra": "allow"}


class TeamListResponse(BaseModel):
    """Paginated list of team members."""

    data: list[TeamMember]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class InviteResponse(BaseModel):
    """Response from inviting a new team member."""

    user_id: int
    email: str
    role: str
    invite_url: str
    message: str

    model_config = {"extra": "allow"}
