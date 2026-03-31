"""SAM Search Profile resource — CRUD, watchers, trigger, runs, and export."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse
from lendiq.types.sam_profile import (
    SAMFetchRun,
    SAMFetchRunListResponse,
    SAMProfileWatcher,
    SAMSearchProfile,
    SAMSearchProfileListResponse,
)


class SAMProfilesResource(SyncAPIResource):
    """Sync resource for SAM Search Profile endpoints."""

    def create(self, **kwargs: Any) -> SAMSearchProfile:
        """Create a new SAM search profile."""
        data = self._request("POST", "/v1/sam/profiles", json=kwargs)
        return SAMSearchProfile.model_validate(data)

    def list(self, *, page: int = 1, per_page: int = 25) -> SAMSearchProfileListResponse:
        """List SAM search profiles for the organization."""
        data = self._request(
            "GET",
            "/v1/sam/profiles",
            params={"page": page, "per_page": per_page},
        )
        return SAMSearchProfileListResponse.model_validate(data)

    def get(self, profile_id: int) -> SAMSearchProfile:
        """Get a SAM search profile by ID."""
        data = self._request("GET", f"/v1/sam/profiles/{profile_id}")
        return SAMSearchProfile.model_validate(data)

    def update(self, profile_id: int, **kwargs: Any) -> SAMSearchProfile:
        """Update a SAM search profile."""
        data = self._request("PATCH", f"/v1/sam/profiles/{profile_id}", json=kwargs)
        return SAMSearchProfile.model_validate(data)

    def delete(self, profile_id: int) -> ActionResponse:
        """Archive a SAM search profile (soft delete)."""
        data = self._request("DELETE", f"/v1/sam/profiles/{profile_id}")
        return ActionResponse.model_validate(data)

    def add_watcher(self, profile_id: int, **kwargs: Any) -> SAMProfileWatcher:
        """Add a watcher to a SAM search profile."""
        data = self._request(
            "POST", f"/v1/sam/profiles/{profile_id}/watchers", json=kwargs
        )
        return SAMProfileWatcher.model_validate(data)

    def remove_watcher(self, profile_id: int, user_id: int) -> ActionResponse:
        """Remove a watcher from a SAM search profile."""
        data = self._request(
            "DELETE", f"/v1/sam/profiles/{profile_id}/watchers/{user_id}"
        )
        return ActionResponse.model_validate(data)

    def trigger(self, profile_id: int) -> SAMFetchRun:
        """Manually trigger a SAM fetch run for this profile."""
        data = self._request("POST", f"/v1/sam/profiles/{profile_id}/trigger")
        return SAMFetchRun.model_validate(data)

    def list_runs(
        self, profile_id: int, *, page: int = 1, per_page: int = 25
    ) -> SAMFetchRunListResponse:
        """List SAM fetch runs triggered by this profile."""
        data = self._request(
            "GET",
            f"/v1/sam/profiles/{profile_id}/runs",
            params={"page": page, "per_page": per_page},
        )
        return SAMFetchRunListResponse.model_validate(data)

    def export_csv(self, profile_id: int, **kwargs: Any) -> bytes:
        """Download a CSV export of SAM entities for this profile."""
        params: dict[str, Any] = {}
        for key in ("run_id", "min_score", "max_score", "state_code", "naics_code"):
            if key in kwargs and kwargs[key] is not None:
                params[key] = kwargs[key]
        return self._request(
            "GET", f"/v1/sam/profiles/{profile_id}/export/csv", params=params, raw=True
        )

    def export_entities_csv(self, **kwargs: Any) -> bytes:
        """Download a CSV export of all SAM entities with optional filters."""
        params: dict[str, Any] = {}
        for key in (
            "profile_id",
            "run_id",
            "min_score",
            "max_score",
            "state_code",
            "naics_code",
            "status",
            "date_from",
            "date_to",
        ):
            if key in kwargs and kwargs[key] is not None:
                params[key] = kwargs[key]
        return self._request(
            "GET", "/v1/sam/entities/export/csv", params=params, raw=True
        )


class AsyncSAMProfilesResource(AsyncAPIResource):
    """Async resource for SAM Search Profile endpoints."""

    async def create(self, **kwargs: Any) -> SAMSearchProfile:
        """Create a new SAM search profile."""
        data = await self._request("POST", "/v1/sam/profiles", json=kwargs)
        return SAMSearchProfile.model_validate(data)

    async def list(
        self, *, page: int = 1, per_page: int = 25
    ) -> SAMSearchProfileListResponse:
        """List SAM search profiles for the organization."""
        data = await self._request(
            "GET",
            "/v1/sam/profiles",
            params={"page": page, "per_page": per_page},
        )
        return SAMSearchProfileListResponse.model_validate(data)

    async def get(self, profile_id: int) -> SAMSearchProfile:
        """Get a SAM search profile by ID."""
        data = await self._request("GET", f"/v1/sam/profiles/{profile_id}")
        return SAMSearchProfile.model_validate(data)

    async def update(self, profile_id: int, **kwargs: Any) -> SAMSearchProfile:
        """Update a SAM search profile."""
        data = await self._request(
            "PATCH", f"/v1/sam/profiles/{profile_id}", json=kwargs
        )
        return SAMSearchProfile.model_validate(data)

    async def delete(self, profile_id: int) -> ActionResponse:
        """Archive a SAM search profile (soft delete)."""
        data = await self._request("DELETE", f"/v1/sam/profiles/{profile_id}")
        return ActionResponse.model_validate(data)

    async def add_watcher(self, profile_id: int, **kwargs: Any) -> SAMProfileWatcher:
        """Add a watcher to a SAM search profile."""
        data = await self._request(
            "POST", f"/v1/sam/profiles/{profile_id}/watchers", json=kwargs
        )
        return SAMProfileWatcher.model_validate(data)

    async def remove_watcher(self, profile_id: int, user_id: int) -> ActionResponse:
        """Remove a watcher from a SAM search profile."""
        data = await self._request(
            "DELETE", f"/v1/sam/profiles/{profile_id}/watchers/{user_id}"
        )
        return ActionResponse.model_validate(data)

    async def trigger(self, profile_id: int) -> SAMFetchRun:
        """Manually trigger a SAM fetch run for this profile."""
        data = await self._request("POST", f"/v1/sam/profiles/{profile_id}/trigger")
        return SAMFetchRun.model_validate(data)

    async def list_runs(
        self, profile_id: int, *, page: int = 1, per_page: int = 25
    ) -> SAMFetchRunListResponse:
        """List SAM fetch runs triggered by this profile."""
        data = await self._request(
            "GET",
            f"/v1/sam/profiles/{profile_id}/runs",
            params={"page": page, "per_page": per_page},
        )
        return SAMFetchRunListResponse.model_validate(data)

    async def export_csv(self, profile_id: int, **kwargs: Any) -> bytes:
        """Download a CSV export of SAM entities for this profile."""
        params: dict[str, Any] = {}
        for key in ("run_id", "min_score", "max_score", "state_code", "naics_code"):
            if key in kwargs and kwargs[key] is not None:
                params[key] = kwargs[key]
        return await self._request(
            "GET", f"/v1/sam/profiles/{profile_id}/export/csv", params=params, raw=True
        )

    async def export_entities_csv(self, **kwargs: Any) -> bytes:
        """Download a CSV export of all SAM entities with optional filters."""
        params: dict[str, Any] = {}
        for key in (
            "profile_id",
            "run_id",
            "min_score",
            "max_score",
            "state_code",
            "naics_code",
            "status",
            "date_from",
            "date_to",
        ):
            if key in kwargs and kwargs[key] is not None:
                params[key] = kwargs[key]
        return await self._request(
            "GET", "/v1/sam/entities/export/csv", params=params, raw=True
        )
