"""Notification response types."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from lendiq.types.common import PaginationMeta


class Notification(BaseModel):
    """An in-app notification."""

    id: int
    notification_type: str
    status: str
    title: str
    body: str | None = None
    url: str | None = None
    resource_type: str | None = None
    resource_id: int | None = None
    created_at: datetime | None = None
    read_at: datetime | None = None

    model_config = {"extra": "allow"}


class NotificationListResponse(BaseModel):
    """Paginated list of notifications."""

    data: list[Notification]
    meta: PaginationMeta

    model_config = {"extra": "allow"}


class UnreadCountResponse(BaseModel):
    """Unread notification count."""

    count: int

    model_config = {"extra": "allow"}


class NotificationPreference(BaseModel):
    """Notification delivery preferences for a single notification type."""

    notification_type: str
    in_app: bool
    email: bool
    push: bool
    slack: bool
    teams: bool
    sms: bool

    model_config = {"extra": "allow"}


class AllPreferencesResponse(BaseModel):
    """All notification preferences keyed by notification type."""

    preferences: dict[str, dict[str, bool]]

    model_config = {"extra": "allow"}
