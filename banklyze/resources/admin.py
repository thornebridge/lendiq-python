"""Admin resource — system health, error logs, usage analytics, and constraints.

Contains both synchronous (AdminResource) and asynchronous (AsyncAdminResource)
implementations. Most endpoints return untyped dicts because the backend does not
define response_model schemas for them. Typed models are used where available.
"""

from __future__ import annotations

import warnings
from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource


# ── Sync resource ────────────────────────────────────────────────────────────


class AdminResource(SyncAPIResource):

    def health(self) -> dict[str, Any]:
        """Get system health: DB connectivity, pipeline success rate, queue depth.

        Returns a dict with keys: ``db_connected``, ``pipeline_success_rate_24h``,
        ``pipelines_last_24h``, ``queue_depth``.
        """
        return self._request("GET", "/v1/admin/health")

    def errors(
        self,
        *,
        severity: str | None = None,
        source: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
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
        return self._request("GET", "/v1/admin/errors", params=params)

    def usage_summary(self, *, days: int = 30) -> dict[str, Any]:
        """Get usage summary for the given period.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        return self._request("GET", "/v1/admin/usage/summary", params={"days": days})

    def usage_daily(self, *, days: int = 30) -> dict[str, Any]:
        """Get daily usage breakdown.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        return self._request("GET", "/v1/admin/usage/daily", params={"days": days})

    def usage_models(self, *, days: int = 30) -> dict[str, Any]:
        """Get usage breakdown by model.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        return self._request("GET", "/v1/admin/usage/models", params={"days": days})

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
    ) -> dict[str, Any]:
        """List dead-letter queue entries."""
        return self._request(
            "GET", "/v1/admin/dlq",
            params={"status": status, "task_name": task_name, "page": page, "per_page": per_page},
        )

    def dlq_retry(self, entry_id: int) -> dict[str, Any]:
        """Retry a failed DLQ entry."""
        return self._request("POST", f"/v1/admin/dlq/{entry_id}/retry")

    def dlq_discard(self, entry_id: int) -> dict[str, Any]:
        """Discard a DLQ entry."""
        return self._request("POST", f"/v1/admin/dlq/{entry_id}/discard")


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncAdminResource(AsyncAPIResource):

    async def health(self) -> dict[str, Any]:
        """Get system health: DB connectivity, pipeline success rate, queue depth.

        Returns a dict with keys: ``db_connected``, ``pipeline_success_rate_24h``,
        ``pipelines_last_24h``, ``queue_depth``.
        """
        return await self._request("GET", "/v1/admin/health")

    async def errors(
        self,
        *,
        severity: str | None = None,
        source: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
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
        return await self._request("GET", "/v1/admin/errors", params=params)

    async def usage_summary(self, *, days: int = 30) -> dict[str, Any]:
        """Get usage summary for the given period.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        return await self._request("GET", "/v1/admin/usage/summary", params={"days": days})

    async def usage_daily(self, *, days: int = 30) -> dict[str, Any]:
        """Get daily usage breakdown.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        return await self._request("GET", "/v1/admin/usage/daily", params={"days": days})

    async def usage_models(self, *, days: int = 30) -> dict[str, Any]:
        """Get usage breakdown by model.

        Args:
            days: Lookback period in days (1-365, default 30).
        """
        return await self._request("GET", "/v1/admin/usage/models", params={"days": days})

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
    ) -> dict[str, Any]:
        """List dead-letter queue entries."""
        return await self._request(
            "GET", "/v1/admin/dlq",
            params={"status": status, "task_name": task_name, "page": page, "per_page": per_page},
        )

    async def dlq_retry(self, entry_id: int) -> dict[str, Any]:
        """Retry a failed DLQ entry."""
        return await self._request("POST", f"/v1/admin/dlq/{entry_id}/retry")

    async def dlq_discard(self, entry_id: int) -> dict[str, Any]:
        """Discard a DLQ entry."""
        return await self._request("POST", f"/v1/admin/dlq/{entry_id}/discard")
