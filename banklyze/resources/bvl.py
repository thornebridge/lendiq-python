"""BVL (Banklyze Validation Layer) resource — batch and on-demand lead validation."""

from __future__ import annotations

from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.bvl import (
    BVLResult,
    BVLRun,
    BVLRunListResponse,
    BVLStats,
    CallQueueResponse,
    SAMEntityListResponse,
    SAMStatsResponse,
)
from banklyze.types.sam_profile import SAMFetchRun, SAMFetchRunListResponse


class BVLResource(SyncAPIResource):
    """Sync resource for BVL lead validation endpoints."""

    def create_run(self, **kwargs: Any) -> BVLRun:
        """Start a batch BVL validation run for all eligible deals."""
        data = self._request("POST", "/v1/bvl/runs", json=kwargs)
        return BVLRun.model_validate(data)

    def list_runs(self, *, page: int = 1, per_page: int = 25) -> BVLRunListResponse:
        """List BVL validation runs."""
        data = self._request(
            "GET",
            "/v1/bvl/runs",
            params={"page": page, "per_page": per_page},
        )
        return BVLRunListResponse.model_validate(data)

    def get_run(self, run_id: int) -> BVLRun:
        """Get status and progress for a BVL validation run."""
        data = self._request("GET", f"/v1/bvl/runs/{run_id}")
        return BVLRun.model_validate(data)

    def cancel_run(self, run_id: int) -> BVLRun:
        """Cancel a running BVL validation batch."""
        data = self._request("POST", f"/v1/bvl/runs/{run_id}/cancel")
        return BVLRun.model_validate(data)

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
        data = self._request("GET", "/v1/bvl/call-queue", params=params)
        return CallQueueResponse.model_validate(data)

    def stats(self) -> BVLStats:
        """Get BVL validation statistics for the organization."""
        data = self._request("GET", "/v1/bvl/stats")
        return BVLStats.model_validate(data)

    def get_result(self, deal_id: int) -> BVLResult:
        """Get BVL validation result for a specific deal."""
        data = self._request("GET", f"/v1/bvl/{deal_id}")
        return BVLResult.model_validate(data)

    def validate(self, deal_id: int, **kwargs: Any) -> BVLResult:
        """Run on-demand BVL validation on a single deal."""
        data = self._request("POST", f"/v1/bvl/{deal_id}/validate", json=kwargs)
        return BVLResult.model_validate(data)

    # ── SAM (via BVL) ────────────────────────────────────────────────────

    def sam_create_run(self, **kwargs: Any) -> SAMFetchRun:
        """Start a SAM entity fetch run via the BVL pipeline."""
        data = self._request("POST", "/v1/bvl/sam/runs", json=kwargs)
        return SAMFetchRun.model_validate(data)

    def sam_list_runs(self, *, page: int = 1, per_page: int = 25) -> SAMFetchRunListResponse:
        """List SAM entity fetch runs."""
        data = self._request(
            "GET", "/v1/bvl/sam/runs",
            params={"page": page, "per_page": per_page},
        )
        return SAMFetchRunListResponse.model_validate(data)

    def sam_get_run(self, run_id: int) -> SAMFetchRun:
        """Get a SAM entity fetch run by ID."""
        data = self._request("GET", f"/v1/bvl/sam/runs/{run_id}")
        return SAMFetchRun.model_validate(data)

    def sam_cancel_run(self, run_id: int) -> SAMFetchRun:
        """Cancel a SAM entity fetch run."""
        data = self._request("POST", f"/v1/bvl/sam/runs/{run_id}/cancel")
        return SAMFetchRun.model_validate(data)

    def sam_entities(self, *, page: int = 1, per_page: int = 25) -> SAMEntityListResponse:
        """List SAM entities discovered by BVL runs."""
        data = self._request(
            "GET", "/v1/bvl/sam/entities",
            params={"page": page, "per_page": per_page},
        )
        return SAMEntityListResponse.model_validate(data)

    def sam_stats(self) -> SAMStatsResponse:
        """Get SAM entity fetch statistics."""
        data = self._request("GET", "/v1/bvl/sam/stats")
        return SAMStatsResponse.model_validate(data)


class AsyncBVLResource(AsyncAPIResource):
    """Async resource for BVL lead validation endpoints."""

    async def create_run(self, **kwargs: Any) -> BVLRun:
        """Start a batch BVL validation run for all eligible deals."""
        data = await self._request("POST", "/v1/bvl/runs", json=kwargs)
        return BVLRun.model_validate(data)

    async def list_runs(
        self, *, page: int = 1, per_page: int = 25
    ) -> BVLRunListResponse:
        """List BVL validation runs."""
        data = await self._request(
            "GET",
            "/v1/bvl/runs",
            params={"page": page, "per_page": per_page},
        )
        return BVLRunListResponse.model_validate(data)

    async def get_run(self, run_id: int) -> BVLRun:
        """Get status and progress for a BVL validation run."""
        data = await self._request("GET", f"/v1/bvl/runs/{run_id}")
        return BVLRun.model_validate(data)

    async def cancel_run(self, run_id: int) -> BVLRun:
        """Cancel a running BVL validation batch."""
        data = await self._request("POST", f"/v1/bvl/runs/{run_id}/cancel")
        return BVLRun.model_validate(data)

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
        data = await self._request("GET", "/v1/bvl/call-queue", params=params)
        return CallQueueResponse.model_validate(data)

    async def stats(self) -> BVLStats:
        """Get BVL validation statistics for the organization."""
        data = await self._request("GET", "/v1/bvl/stats")
        return BVLStats.model_validate(data)

    async def get_result(self, deal_id: int) -> BVLResult:
        """Get BVL validation result for a specific deal."""
        data = await self._request("GET", f"/v1/bvl/{deal_id}")
        return BVLResult.model_validate(data)

    async def validate(self, deal_id: int, **kwargs: Any) -> BVLResult:
        """Run on-demand BVL validation on a single deal."""
        data = await self._request(
            "POST", f"/v1/bvl/{deal_id}/validate", json=kwargs
        )
        return BVLResult.model_validate(data)

    # ── SAM (via BVL) ────────────────────────────────────────────────────

    async def sam_create_run(self, **kwargs: Any) -> SAMFetchRun:
        """Start a SAM entity fetch run via the BVL pipeline."""
        data = await self._request("POST", "/v1/bvl/sam/runs", json=kwargs)
        return SAMFetchRun.model_validate(data)

    async def sam_list_runs(self, *, page: int = 1, per_page: int = 25) -> SAMFetchRunListResponse:
        """List SAM entity fetch runs."""
        data = await self._request(
            "GET", "/v1/bvl/sam/runs",
            params={"page": page, "per_page": per_page},
        )
        return SAMFetchRunListResponse.model_validate(data)

    async def sam_get_run(self, run_id: int) -> SAMFetchRun:
        """Get a SAM entity fetch run by ID."""
        data = await self._request("GET", f"/v1/bvl/sam/runs/{run_id}")
        return SAMFetchRun.model_validate(data)

    async def sam_cancel_run(self, run_id: int) -> SAMFetchRun:
        """Cancel a SAM entity fetch run."""
        data = await self._request("POST", f"/v1/bvl/sam/runs/{run_id}/cancel")
        return SAMFetchRun.model_validate(data)

    async def sam_entities(self, *, page: int = 1, per_page: int = 25) -> SAMEntityListResponse:
        """List SAM entities discovered by BVL runs."""
        data = await self._request(
            "GET", "/v1/bvl/sam/entities",
            params={"page": page, "per_page": per_page},
        )
        return SAMEntityListResponse.model_validate(data)

    async def sam_stats(self) -> SAMStatsResponse:
        """Get SAM entity fetch statistics."""
        data = await self._request("GET", "/v1/bvl/sam/stats")
        return SAMStatsResponse.model_validate(data)
