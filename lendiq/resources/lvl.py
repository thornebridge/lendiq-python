"""LVL (LendIQ Validation Layer) resource — batch and on-demand lead validation."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.lvl import (
    LVLResult,
    LVLRun,
    LVLRunListResponse,
    LVLStats,
    CallQueueResponse,
    SAMEntityListResponse,
    SAMStatsResponse,
)
from lendiq.types.sam_profile import SAMFetchRun, SAMFetchRunListResponse


class LVLResource(SyncAPIResource):
    """Sync resource for LVL lead validation endpoints."""

    def create_run(self, **kwargs: Any) -> LVLRun:
        """Start a batch LVL validation run for all eligible deals."""
        data = self._request("POST", "/v1/lvl/runs", json=kwargs)
        return LVLRun.model_validate(data)

    def list_runs(self, *, page: int = 1, per_page: int = 25) -> LVLRunListResponse:
        """List LVL validation runs."""
        data = self._request(
            "GET",
            "/v1/lvl/runs",
            params={"page": page, "per_page": per_page},
        )
        return LVLRunListResponse.model_validate(data)

    def get_run(self, run_id: int) -> LVLRun:
        """Get status and progress for a LVL validation run."""
        data = self._request("GET", f"/v1/lvl/runs/{run_id}")
        return LVLRun.model_validate(data)

    def cancel_run(self, run_id: int) -> LVLRun:
        """Cancel a running LVL validation batch."""
        data = self._request("POST", f"/v1/lvl/runs/{run_id}/cancel")
        return LVLRun.model_validate(data)

    def call_queue(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
        tier: str | None = None,
        state: str | None = None,
        industry: str | None = None,
        min_score: float | None = None,
        max_score: float | None = None,
        include_disqualified: bool = False,
    ) -> CallQueueResponse:
        """Get prioritized call queue of validated leads."""
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if tier is not None:
            params["tier"] = tier
        if state is not None:
            params["state"] = state
        if industry is not None:
            params["industry"] = industry
        if min_score is not None:
            params["min_score"] = min_score
        if max_score is not None:
            params["max_score"] = max_score
        if include_disqualified:
            params["include_disqualified"] = True
        data = self._request("GET", "/v1/lvl/call-queue", params=params)
        return CallQueueResponse.model_validate(data)

    def stats(self) -> LVLStats:
        """Get LVL validation statistics for the organization."""
        data = self._request("GET", "/v1/lvl/stats")
        return LVLStats.model_validate(data)

    def get_result(self, deal_id: int) -> LVLResult:
        """Get LVL validation result for a specific deal."""
        data = self._request("GET", f"/v1/lvl/{deal_id}")
        return LVLResult.model_validate(data)

    def validate(self, deal_id: int, **kwargs: Any) -> LVLResult:
        """Run on-demand LVL validation on a single deal."""
        data = self._request("POST", f"/v1/lvl/{deal_id}/validate", json=kwargs)
        return LVLResult.model_validate(data)

    # ── SAM (via LVL) ────────────────────────────────────────────────────

    def sam_create_run(self, **kwargs: Any) -> SAMFetchRun:
        """Start a SAM entity fetch run via the LVL pipeline."""
        data = self._request("POST", "/v1/lvl/sam/runs", json=kwargs)
        return SAMFetchRun.model_validate(data)

    def sam_list_runs(self, *, page: int = 1, per_page: int = 25) -> SAMFetchRunListResponse:
        """List SAM entity fetch runs."""
        data = self._request(
            "GET", "/v1/lvl/sam/runs",
            params={"page": page, "per_page": per_page},
        )
        return SAMFetchRunListResponse.model_validate(data)

    def sam_get_run(self, run_id: int) -> SAMFetchRun:
        """Get a SAM entity fetch run by ID."""
        data = self._request("GET", f"/v1/lvl/sam/runs/{run_id}")
        return SAMFetchRun.model_validate(data)

    def sam_cancel_run(self, run_id: int) -> SAMFetchRun:
        """Cancel a SAM entity fetch run."""
        data = self._request("POST", f"/v1/lvl/sam/runs/{run_id}/cancel")
        return SAMFetchRun.model_validate(data)

    def sam_entities(self, *, page: int = 1, per_page: int = 25) -> SAMEntityListResponse:
        """List SAM entities discovered by LVL runs."""
        data = self._request(
            "GET", "/v1/lvl/sam/entities",
            params={"page": page, "per_page": per_page},
        )
        return SAMEntityListResponse.model_validate(data)

    def sam_stats(self) -> SAMStatsResponse:
        """Get SAM entity fetch statistics."""
        data = self._request("GET", "/v1/lvl/sam/stats")
        return SAMStatsResponse.model_validate(data)


class AsyncLVLResource(AsyncAPIResource):
    """Async resource for LVL lead validation endpoints."""

    async def create_run(self, **kwargs: Any) -> LVLRun:
        """Start a batch LVL validation run for all eligible deals."""
        data = await self._request("POST", "/v1/lvl/runs", json=kwargs)
        return LVLRun.model_validate(data)

    async def list_runs(
        self, *, page: int = 1, per_page: int = 25
    ) -> LVLRunListResponse:
        """List LVL validation runs."""
        data = await self._request(
            "GET",
            "/v1/lvl/runs",
            params={"page": page, "per_page": per_page},
        )
        return LVLRunListResponse.model_validate(data)

    async def get_run(self, run_id: int) -> LVLRun:
        """Get status and progress for a LVL validation run."""
        data = await self._request("GET", f"/v1/lvl/runs/{run_id}")
        return LVLRun.model_validate(data)

    async def cancel_run(self, run_id: int) -> LVLRun:
        """Cancel a running LVL validation batch."""
        data = await self._request("POST", f"/v1/lvl/runs/{run_id}/cancel")
        return LVLRun.model_validate(data)

    async def call_queue(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
        tier: str | None = None,
        state: str | None = None,
        industry: str | None = None,
        min_score: float | None = None,
        max_score: float | None = None,
        include_disqualified: bool = False,
    ) -> CallQueueResponse:
        """Get prioritized call queue of validated leads."""
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if tier is not None:
            params["tier"] = tier
        if state is not None:
            params["state"] = state
        if industry is not None:
            params["industry"] = industry
        if min_score is not None:
            params["min_score"] = min_score
        if max_score is not None:
            params["max_score"] = max_score
        if include_disqualified:
            params["include_disqualified"] = True
        data = await self._request("GET", "/v1/lvl/call-queue", params=params)
        return CallQueueResponse.model_validate(data)

    async def stats(self) -> LVLStats:
        """Get LVL validation statistics for the organization."""
        data = await self._request("GET", "/v1/lvl/stats")
        return LVLStats.model_validate(data)

    async def get_result(self, deal_id: int) -> LVLResult:
        """Get LVL validation result for a specific deal."""
        data = await self._request("GET", f"/v1/lvl/{deal_id}")
        return LVLResult.model_validate(data)

    async def validate(self, deal_id: int, **kwargs: Any) -> LVLResult:
        """Run on-demand LVL validation on a single deal."""
        data = await self._request(
            "POST", f"/v1/lvl/{deal_id}/validate", json=kwargs
        )
        return LVLResult.model_validate(data)

    # ── SAM (via LVL) ────────────────────────────────────────────────────

    async def sam_create_run(self, **kwargs: Any) -> SAMFetchRun:
        """Start a SAM entity fetch run via the LVL pipeline."""
        data = await self._request("POST", "/v1/lvl/sam/runs", json=kwargs)
        return SAMFetchRun.model_validate(data)

    async def sam_list_runs(self, *, page: int = 1, per_page: int = 25) -> SAMFetchRunListResponse:
        """List SAM entity fetch runs."""
        data = await self._request(
            "GET", "/v1/lvl/sam/runs",
            params={"page": page, "per_page": per_page},
        )
        return SAMFetchRunListResponse.model_validate(data)

    async def sam_get_run(self, run_id: int) -> SAMFetchRun:
        """Get a SAM entity fetch run by ID."""
        data = await self._request("GET", f"/v1/lvl/sam/runs/{run_id}")
        return SAMFetchRun.model_validate(data)

    async def sam_cancel_run(self, run_id: int) -> SAMFetchRun:
        """Cancel a SAM entity fetch run."""
        data = await self._request("POST", f"/v1/lvl/sam/runs/{run_id}/cancel")
        return SAMFetchRun.model_validate(data)

    async def sam_entities(self, *, page: int = 1, per_page: int = 25) -> SAMEntityListResponse:
        """List SAM entities discovered by LVL runs."""
        data = await self._request(
            "GET", "/v1/lvl/sam/entities",
            params={"page": page, "per_page": per_page},
        )
        return SAMEntityListResponse.model_validate(data)

    async def sam_stats(self) -> SAMStatsResponse:
        """Get SAM entity fetch statistics."""
        data = await self._request("GET", "/v1/lvl/sam/stats")
        return SAMStatsResponse.model_validate(data)
