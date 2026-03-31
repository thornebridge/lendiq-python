"""Notifications resource — list, mark read, and manage preferences."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse
from lendiq.types.notification import (
    AllPreferencesResponse,
    NotificationListResponse,
    NotificationPreference,
    UnreadCountResponse,
)


class NotificationsResource(SyncAPIResource):

    def list(
        self,
        *,
        status: str | None = None,
        page: int = 1,
        per_page: int = 25,
    ) -> NotificationListResponse:
        """List notifications for the current user.

        Args:
            status: Filter by status — ``"unread"`` or ``"read"``.
            page: Page number (default 1).
            per_page: Results per page (default 25, max 100).
        """
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if status is not None:
            params["status"] = status
        data = self._request("GET", "/v1/notifications", params=params)
        return NotificationListResponse.model_validate(data)

    def unread_count(self) -> UnreadCountResponse:
        """Get the count of unread notifications."""
        data = self._request("GET", "/v1/notifications/unread-count")
        return UnreadCountResponse.model_validate(data)

    def mark_read(self, notification_ids: list[int]) -> ActionResponse:
        """Mark specific notifications as read.

        Args:
            notification_ids: List of notification IDs to mark as read (1--100).
        """
        data = self._request(
            "POST",
            "/v1/notifications/mark-read",
            json={"notification_ids": notification_ids},
        )
        return ActionResponse.model_validate(data)

    def mark_all_read(self) -> ActionResponse:
        """Mark all notifications as read for the current user."""
        data = self._request("POST", "/v1/notifications/mark-all-read")
        return ActionResponse.model_validate(data)

    def get_preferences(self) -> AllPreferencesResponse:
        """Get all notification delivery preferences."""
        data = self._request("GET", "/v1/notifications/preferences")
        return AllPreferencesResponse.model_validate(data)

    def update_preference(
        self,
        notification_type: str,
        *,
        in_app: bool | None = None,
        email: bool | None = None,
        push: bool | None = None,
        slack: bool | None = None,
        teams: bool | None = None,
        sms: bool | None = None,
    ) -> NotificationPreference:
        """Update delivery preferences for a notification type.

        Args:
            notification_type: The notification type to configure (e.g. ``"deal_assigned"``).
            in_app: Enable/disable in-app delivery.
            email: Enable/disable email delivery.
            push: Enable/disable push notification delivery.
            slack: Enable/disable Slack delivery.
            teams: Enable/disable Microsoft Teams delivery.
            sms: Enable/disable SMS delivery.
        """
        body: dict[str, Any] = {}
        if in_app is not None:
            body["in_app"] = in_app
        if email is not None:
            body["email"] = email
        if push is not None:
            body["push"] = push
        if slack is not None:
            body["slack"] = slack
        if teams is not None:
            body["teams"] = teams
        if sms is not None:
            body["sms"] = sms
        data = self._request(
            "PUT",
            f"/v1/notifications/preferences/{notification_type}",
            json=body,
        )
        return NotificationPreference.model_validate(data)


class AsyncNotificationsResource(AsyncAPIResource):

    async def list(
        self,
        *,
        status: str | None = None,
        page: int = 1,
        per_page: int = 25,
    ) -> NotificationListResponse:
        """List notifications for the current user.

        Args:
            status: Filter by status — ``"unread"`` or ``"read"``.
            page: Page number (default 1).
            per_page: Results per page (default 25, max 100).
        """
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if status is not None:
            params["status"] = status
        data = await self._request("GET", "/v1/notifications", params=params)
        return NotificationListResponse.model_validate(data)

    async def unread_count(self) -> UnreadCountResponse:
        """Get the count of unread notifications."""
        data = await self._request("GET", "/v1/notifications/unread-count")
        return UnreadCountResponse.model_validate(data)

    async def mark_read(self, notification_ids: list[int]) -> ActionResponse:
        """Mark specific notifications as read.

        Args:
            notification_ids: List of notification IDs to mark as read (1--100).
        """
        data = await self._request(
            "POST",
            "/v1/notifications/mark-read",
            json={"notification_ids": notification_ids},
        )
        return ActionResponse.model_validate(data)

    async def mark_all_read(self) -> ActionResponse:
        """Mark all notifications as read for the current user."""
        data = await self._request("POST", "/v1/notifications/mark-all-read")
        return ActionResponse.model_validate(data)

    async def get_preferences(self) -> AllPreferencesResponse:
        """Get all notification delivery preferences."""
        data = await self._request("GET", "/v1/notifications/preferences")
        return AllPreferencesResponse.model_validate(data)

    async def update_preference(
        self,
        notification_type: str,
        *,
        in_app: bool | None = None,
        email: bool | None = None,
        push: bool | None = None,
        slack: bool | None = None,
        teams: bool | None = None,
        sms: bool | None = None,
    ) -> NotificationPreference:
        """Update delivery preferences for a notification type.

        Args:
            notification_type: The notification type to configure (e.g. ``"deal_assigned"``).
            in_app: Enable/disable in-app delivery.
            email: Enable/disable email delivery.
            push: Enable/disable push notification delivery.
            slack: Enable/disable Slack delivery.
            teams: Enable/disable Microsoft Teams delivery.
            sms: Enable/disable SMS delivery.
        """
        body: dict[str, Any] = {}
        if in_app is not None:
            body["in_app"] = in_app
        if email is not None:
            body["email"] = email
        if push is not None:
            body["push"] = push
        if slack is not None:
            body["slack"] = slack
        if teams is not None:
            body["teams"] = teams
        if sms is not None:
            body["sms"] = sms
        data = await self._request(
            "PUT",
            f"/v1/notifications/preferences/{notification_type}",
            json=body,
        )
        return NotificationPreference.model_validate(data)
