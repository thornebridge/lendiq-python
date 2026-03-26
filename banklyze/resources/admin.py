"""Admin resource — system health, error logs, usage analytics, and constraints.

Contains both synchronous (AdminResource) and asynchronous (AsyncAdminResource)
implementations. Most endpoints return untyped dicts because the backend does not
define response_model schemas for them. Typed models are used where available.
"""

from __future__ import annotations

import warnings
from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.admin import (
    ErrorLogListResponse,
    HealthResponse,
    UsageDailyResponse,
    UsageModelsResponse,
    UsageSummaryResponse,
)
from banklyze.types.dlq import DlqActionResponse, DlqListResponse


# ── Sync resource ────────────────────────────────────────────────────────────


class AdminResource(SyncAPIResource):

    def health(self) -> HealthResponse:
        """Get system health: DB connectivity, pipeline success rate, queue depth.

        Returns a dict with keys: ``db_connected``, ``pipeline_success_rate_24h``,
        ``pipelines_last_24h``, ``queue_depth``.
        """
        data = self._request("GET", "/v1/admin/health")
        return HealthResponse.model_validate(data)

    def errors(
        self,
        *,
        severity: str | None = None,
        source: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> ErrorLogListResponse:
        """List recent error log entries.

        Args:
            severity: Filter by severity (e.g. ``"error"``, ``"warning"``).
            source: Filter by error source (e.g. ``"pipeline"``).
            limit: Maximum number of entries to return (1-100, default 20).
            offset: Pagination offset (default 0).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if severity is not None:
            params["severity"] = severity
        if source is not None:
            params["source"] = source
        data = self._request("GET", "/v1/admin/errors", params=params)
        return ErrorLogListResponse.model_validate(data)

    def usage_summary(self, *, days: int = 30) -> UsageSummaryResponse:
        """Get usage summary for the given period.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        data = self._request("GET", "/v1/admin/usage/summary", params={"days": days})
        return UsageSummaryResponse.model_validate(data)

    def usage_daily(self, *, days: int = 30) -> UsageDailyResponse:
        """Get daily usage breakdown.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        data = self._request("GET", "/v1/admin/usage/daily", params={"days": days})
        return UsageDailyResponse.model_validate(data)

    def usage_models(self, *, days: int = 30) -> UsageModelsResponse:
        """Get usage breakdown by model.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        data = self._request("GET", "/v1/admin/usage/models", params={"days": days})
        return UsageModelsResponse.model_validate(data)

    def get_constraints(self) -> dict[str, Any]:
        """Get underwriting constraint thresholds from the default ruleset.

        .. deprecated::
            Use the rulesets resource instead.
        """
        warnings.warn(
            "get_constraints() is deprecated; use client.rulesets.list() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._request("GET", "/v1/admin/constraints")

    def update_constraints(self, **kwargs: Any) -> dict[str, Any]:
        """Update underwriting constraint thresholds on the default ruleset.

        Pass constraint fields as keyword arguments. Only provided fields are
        updated; omitted fields are left unchanged.

        .. deprecated::
            Use the rulesets resource instead.

        Keyword Args:
            min_monthly_deposits: Minimum monthly deposit total.
            min_days_covered: Minimum days of coverage.
            min_health_score: Minimum composite health score.
            max_suspicious_count: Maximum suspicious transaction count.
            max_nsf_per_month: Maximum NSFs per month.
            max_debt_service_ratio: Maximum debt-service ratio.
            approve_min_score: Minimum score for auto-approve.
            conditional_min_score: Minimum score for conditional approval.
        """
        warnings.warn(
            "update_constraints() is deprecated; use the client.rulesets resource instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._request("PUT", "/v1/admin/constraints", json=kwargs)

    def dlq_list(
        self,
        *,
        status: str | None = None,
        task_name: str | None = None,
        page: int = 1,
        per_page: int = 25,
    ) -> DlqListResponse:
        """List dead-letter queue entries."""
        data = self._request(
            "GET", "/v1/admin/dlq",
            params={"status": status, "task_name": task_name, "page": page, "per_page": per_page},
        )
        return DlqListResponse.model_validate(data)

    def dlq_retry(self, entry_id: int) -> DlqActionResponse:
        """Retry a failed DLQ entry."""
        data = self._request("POST", f"/v1/admin/dlq/{entry_id}/retry")
        return DlqActionResponse.model_validate(data)

    def dlq_discard(self, entry_id: int) -> DlqActionResponse:
        """Discard a DLQ entry."""
        data = self._request("POST", f"/v1/admin/dlq/{entry_id}/discard")
        return DlqActionResponse.model_validate(data)

    def pipeline_settings(self) -> dict[str, Any]:
        """Get pipeline settings for the current organization."""
        return self._request("GET", "/v1/admin/pipeline-settings")

    def update_pipeline_settings(self, **kwargs: Any) -> dict[str, Any]:
        """Update pipeline settings for the current organization.

        Keyword Args:
            pipeline_llm: Enable/disable LLM extraction.
            pipeline_vision: Enable/disable vision fallback.
            pipeline_ai_screening: Enable/disable AI-powered screening.
        """
        return self._request("PUT", "/v1/admin/pipeline-settings", json=kwargs)


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncAdminResource(AsyncAPIResource):

    async def health(self) -> HealthResponse:
        """Get system health: DB connectivity, pipeline success rate, queue depth.

        Returns a dict with keys: ``db_connected``, ``pipeline_success_rate_24h``,
        ``pipelines_last_24h``, ``queue_depth``.
        """
        data = await self._request("GET", "/v1/admin/health")
        return HealthResponse.model_validate(data)

    async def errors(
        self,
        *,
        severity: str | None = None,
        source: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> ErrorLogListResponse:
        """List recent error log entries.

        Args:
            severity: Filter by severity (e.g. ``"error"``, ``"warning"``).
            source: Filter by error source (e.g. ``"pipeline"``).
            limit: Maximum number of entries to return (1-100, default 20).
            offset: Pagination offset (default 0).
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if severity is not None:
            params["severity"] = severity
        if source is not None:
            params["source"] = source
        data = await self._request("GET", "/v1/admin/errors", params=params)
        return ErrorLogListResponse.model_validate(data)

    async def usage_summary(self, *, days: int = 30) -> UsageSummaryResponse:
        """Get usage summary for the given period.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        data = await self._request("GET", "/v1/admin/usage/summary", params={"days": days})
        return UsageSummaryResponse.model_validate(data)

    async def usage_daily(self, *, days: int = 30) -> UsageDailyResponse:
        """Get daily usage breakdown.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        data = await self._request("GET", "/v1/admin/usage/daily", params={"days": days})
        return UsageDailyResponse.model_validate(data)

    async def usage_models(self, *, days: int = 30) -> UsageModelsResponse:
        """Get usage breakdown by model.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        data = await self._request("GET", "/v1/admin/usage/models", params={"days": days})
        return UsageModelsResponse.model_validate(data)

    async def get_constraints(self) -> dict[str, Any]:
        """Get underwriting constraint thresholds from the default ruleset.

        .. deprecated::
            Use the rulesets resource instead.
        """
        warnings.warn(
            "get_constraints() is deprecated; use client.rulesets.list() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self._request("GET", "/v1/admin/constraints")

    async def update_constraints(self, **kwargs: Any) -> dict[str, Any]:
        """Update underwriting constraint thresholds on the default ruleset.

        Pass constraint fields as keyword arguments. Only provided fields are
        updated; omitted fields are left unchanged.

        .. deprecated::
            Use the rulesets resource instead.

        Keyword Args:
            min_monthly_deposits: Minimum monthly deposit total.
            min_days_covered: Minimum days of coverage.
            min_health_score: Minimum composite health score.
            max_suspicious_count: Maximum suspicious transaction count.
            max_nsf_per_month: Maximum NSFs per month.
            max_debt_service_ratio: Maximum debt-service ratio.
            approve_min_score: Minimum score for auto-approve.
            conditional_min_score: Minimum score for conditional approval.
        """
        warnings.warn(
            "update_constraints() is deprecated; use the client.rulesets resource instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self._request("PUT", "/v1/admin/constraints", json=kwargs)

    async def dlq_list(
        self,
        *,
        status: str | None = None,
        task_name: str | None = None,
        page: int = 1,
        per_page: int = 25,
    ) -> DlqListResponse:
        """List dead-letter queue entries."""
        data = await self._request(
            "GET", "/v1/admin/dlq",
            params={"status": status, "task_name": task_name, "page": page, "per_page": per_page},
        )
        return DlqListResponse.model_validate(data)

    async def dlq_retry(self, entry_id: int) -> DlqActionResponse:
        """Retry a failed DLQ entry."""
        data = await self._request("POST", f"/v1/admin/dlq/{entry_id}/retry")
        return DlqActionResponse.model_validate(data)

    async def dlq_discard(self, entry_id: int) -> DlqActionResponse:
        """Discard a DLQ entry."""
        data = await self._request("POST", f"/v1/admin/dlq/{entry_id}/discard")
        return DlqActionResponse.model_validate(data)

    async def pipeline_settings(self) -> dict[str, Any]:
        """Get pipeline settings for the current organization."""
        return await self._request("GET", "/v1/admin/pipeline-settings")

    async def update_pipeline_settings(self, **kwargs: Any) -> dict[str, Any]:
        """Update pipeline settings for the current organization.

        Keyword Args:
            pipeline_llm: Enable/disable LLM extraction.
            pipeline_vision: Enable/disable vision fallback.
            pipeline_ai_screening: Enable/disable AI-powered screening.
        """
        return await self._request("PUT", "/v1/admin/pipeline-settings", json=kwargs)
