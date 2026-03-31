"""Team management resource — list, invite, update, deactivate members."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse
from lendiq.types.team import InviteResponse, TeamListResponse, TeamMember


class TeamResource(SyncAPIResource):

    def list(self) -> TeamListResponse:
        """List all members of the current organization."""
        data = self._request("GET", "/v1/team")
        return TeamListResponse.model_validate(data)

    def invite(
        self,
        *,
        email: str,
        role: str = "viewer",
        display_name: str | None = None,
    ) -> InviteResponse:
        """Invite a new member by email."""
        body: dict[str, Any] = {"email": email, "role": role}
        if display_name is not None:
            body["display_name"] = display_name
        data = self._request("POST", "/v1/team/invite", json=body)
        return InviteResponse.model_validate(data)

    def update(
        self,
        user_id: int,
        *,
        role: str | None = None,
        display_name: str | None = None,
    ) -> TeamMember:
        """Update a team member's role or display name."""
        body: dict[str, Any] = {}
        if role is not None:
            body["role"] = role
        if display_name is not None:
            body["display_name"] = display_name
        data = self._request("PATCH", f"/v1/team/{user_id}", json=body)
        return TeamMember.model_validate(data)

    def deactivate(self, user_id: int) -> ActionResponse:
        """Deactivate a team member."""
        data = self._request("DELETE", f"/v1/team/{user_id}")
        return ActionResponse.model_validate(data)


class AsyncTeamResource(AsyncAPIResource):

    async def list(self) -> TeamListResponse:
        """List all members of the current organization."""
        data = await self._request("GET", "/v1/team")
        return TeamListResponse.model_validate(data)

    async def invite(
        self,
        *,
        email: str,
        role: str = "viewer",
        display_name: str | None = None,
    ) -> InviteResponse:
        """Invite a new member by email."""
        body: dict[str, Any] = {"email": email, "role": role}
        if display_name is not None:
            body["display_name"] = display_name
        data = await self._request("POST", "/v1/team/invite", json=body)
        return InviteResponse.model_validate(data)

    async def update(
        self,
        user_id: int,
        *,
        role: str | None = None,
        display_name: str | None = None,
    ) -> TeamMember:
        """Update a team member's role or display name."""
        body: dict[str, Any] = {}
        if role is not None:
            body["role"] = role
        if display_name is not None:
            body["display_name"] = display_name
        data = await self._request("PATCH", f"/v1/team/{user_id}", json=body)
        return TeamMember.model_validate(data)

    async def deactivate(self, user_id: int) -> ActionResponse:
        """Deactivate a team member."""
        data = await self._request("DELETE", f"/v1/team/{user_id}")
        return ActionResponse.model_validate(data)
