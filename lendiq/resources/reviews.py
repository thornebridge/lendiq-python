"""Human review resource — list, detail, approve, correct."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.reviews import (
    ReviewActionResponse,
    ReviewDetailResponse,
    ReviewListResponse,
)


class ReviewsResource(SyncAPIResource):
    """Sync resource for human review endpoints."""

    def list(self, *, page: int = 1, per_page: int = 25, status: str | None = None) -> ReviewListResponse:
        """List documents that need or have had human review."""
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if status is not None:
            params["status"] = status
        data = self._request("GET", "/v1/reviews", params=params)
        return ReviewListResponse.model_validate(data)

    def get(self, doc_id: int) -> ReviewDetailResponse:
        """Get document details for review with all transactions."""
        data = self._request("GET", f"/v1/reviews/{doc_id}")
        return ReviewDetailResponse.model_validate(data)

    def approve(self, doc_id: int) -> ReviewActionResponse:
        """Approve extraction as-is."""
        data = self._request("POST", f"/v1/reviews/{doc_id}/approve")
        return ReviewActionResponse.model_validate(data)

    def correct(self, doc_id: int, *, corrections: list[dict[str, Any]] | None = None, notes: str | None = None) -> ReviewActionResponse:
        """Submit corrections to extracted transactions."""
        body: dict[str, Any] = {}
        if corrections is not None:
            body["corrections"] = corrections
        if notes is not None:
            body["notes"] = notes
        data = self._request("POST", f"/v1/reviews/{doc_id}/correct", json=body)
        return ReviewActionResponse.model_validate(data)


class AsyncReviewsResource(AsyncAPIResource):
    """Async resource for human review endpoints."""

    async def list(self, *, page: int = 1, per_page: int = 25, status: str | None = None) -> ReviewListResponse:
        """List documents that need or have had human review."""
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if status is not None:
            params["status"] = status
        data = await self._request("GET", "/v1/reviews", params=params)
        return ReviewListResponse.model_validate(data)

    async def get(self, doc_id: int) -> ReviewDetailResponse:
        """Get document details for review with all transactions."""
        data = await self._request("GET", f"/v1/reviews/{doc_id}")
        return ReviewDetailResponse.model_validate(data)

    async def approve(self, doc_id: int) -> ReviewActionResponse:
        """Approve extraction as-is."""
        data = await self._request("POST", f"/v1/reviews/{doc_id}/approve")
        return ReviewActionResponse.model_validate(data)

    async def correct(self, doc_id: int, *, corrections: list[dict[str, Any]] | None = None, notes: str | None = None) -> ReviewActionResponse:
        """Submit corrections to extracted transactions."""
        body: dict[str, Any] = {}
        if corrections is not None:
            body["corrections"] = corrections
        if notes is not None:
            body["notes"] = notes
        data = await self._request("POST", f"/v1/reviews/{doc_id}/correct", json=body)
        return ReviewActionResponse.model_validate(data)
