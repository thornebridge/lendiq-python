"""Usage resource — org usage summary and processing time analytics.

Contains both synchronous (UsageResource) and asynchronous (AsyncUsageResource)
implementations. All methods return typed Pydantic models.
"""

from __future__ import annotations

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.usage import ProcessingTimeStats, UsageSummary


# ── Sync resource ────────────────────────────────────────────────────────────


class UsageResource(SyncAPIResource):

    def summary(self) -> UsageSummary:
        """Get the enhanced usage summary for the authenticated organization."""
        data = self._request("GET", "/v1/usage/me")
        return UsageSummary.model_validate(data)

    def processing_times(
        self,
        *,
        document_type: str | None = None,
        days: int = 30,
    ) -> ProcessingTimeStats:
        """Get processing time percentiles by document type.

        Args:
            document_type: Optional filter by document type.
            days: Lookback period in days (1-365, default 30).
        """
        params: dict = {"days": days}
        if document_type is not None:
            params["document_type"] = document_type
        data = self._request("GET", "/v1/usage/me/processing-times", params=params)
        return ProcessingTimeStats.model_validate(data)


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncUsageResource(AsyncAPIResource):

    async def summary(self) -> UsageSummary:
        """Get the enhanced usage summary for the authenticated organization."""
        data = await self._request("GET", "/v1/usage/me")
        return UsageSummary.model_validate(data)

    async def processing_times(
        self,
        *,
        document_type: str | None = None,
        days: int = 30,
    ) -> ProcessingTimeStats:
        """Get processing time percentiles by document type.

        Args:
            document_type: Optional filter by document type.
            days: Lookback period in days (1-365, default 30).
        """
        params: dict = {"days": days}
        if document_type is not None:
            params["document_type"] = document_type
        data = await self._request("GET", "/v1/usage/me/processing-times", params=params)
        return ProcessingTimeStats.model_validate(data)
