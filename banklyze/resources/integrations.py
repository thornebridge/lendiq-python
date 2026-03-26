"""Integrations resource — CRUD for org-level integration configs + health dashboard.

Contains both synchronous (IntegrationsResource) and asynchronous
(AsyncIntegrationsResource) implementations. All methods return typed Pydantic models.
"""

from __future__ import annotations

from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.common import ActionResponse
from banklyze.types.integration import Integration, IntegrationHealthResponse, IntegrationTestResponse


# ── Sync resource ────────────────────────────────────────────────────────────


class IntegrationsResource(SyncAPIResource):

    def health(self) -> IntegrationHealthResponse:
        """Get the integration health dashboard.

        Returns webhook delivery rates, API error rates, document quota usage,
        and queue depth.
        """
        data = self._request("GET", "/v1/integrations/health")
        return IntegrationHealthResponse.model_validate(data)

    def list(self) -> list[Integration]:
        """List all integration configurations for the current organization."""
        data = self._request("GET", "/v1/integrations")
        return [Integration.model_validate(item) for item in data.get("integrations", [])]

    def upsert(
        self,
        integration_type: str,
        *,
        enabled: bool | None = None,
        label: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> Integration:
        """Create or update an integration configuration.

        Args:
            integration_type: The integration type (e.g. ``"slack"``, ``"teams"``,
                ``"twilio"``, ``"smtp"``).
            enabled: Whether the integration is enabled.
            label: Optional descriptive label.
            credentials: Credentials dict (encrypted at rest on the server).
        """
        body: dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if label is not None:
            body["label"] = label
        if credentials is not None:
            body["credentials"] = credentials
        data = self._request("PUT", f"/v1/integrations/{integration_type}", json=body)
        return Integration.model_validate(data)

    def delete(self, integration_type: str) -> ActionResponse:
        """Remove an integration configuration.

        Args:
            integration_type: The integration type to remove.
        """
        data = self._request("DELETE", f"/v1/integrations/{integration_type}")
        return ActionResponse.model_validate(data)

    def test(self, integration_type: str) -> IntegrationTestResponse:
        """Send a test notification through the specified integration.

        Args:
            integration_type: The integration type to test.
        """
        data = self._request("POST", f"/v1/integrations/{integration_type}/test")
        return IntegrationTestResponse.model_validate(data)


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncIntegrationsResource(AsyncAPIResource):

    async def health(self) -> IntegrationHealthResponse:
        """Get the integration health dashboard.

        Returns webhook delivery rates, API error rates, document quota usage,
        and queue depth.
        """
        data = await self._request("GET", "/v1/integrations/health")
        return IntegrationHealthResponse.model_validate(data)

    async def list(self) -> list[Integration]:
        """List all integration configurations for the current organization."""
        data = await self._request("GET", "/v1/integrations")
        return [Integration.model_validate(item) for item in data.get("integrations", [])]

    async def upsert(
        self,
        integration_type: str,
        *,
        enabled: bool | None = None,
        label: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> Integration:
        """Create or update an integration configuration.

        Args:
            integration_type: The integration type (e.g. ``"slack"``, ``"teams"``,
                ``"twilio"``, ``"smtp"``).
            enabled: Whether the integration is enabled.
            label: Optional descriptive label.
            credentials: Credentials dict (encrypted at rest on the server).
        """
        body: dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if label is not None:
            body["label"] = label
        if credentials is not None:
            body["credentials"] = credentials
        data = await self._request("PUT", f"/v1/integrations/{integration_type}", json=body)
        return Integration.model_validate(data)

    async def delete(self, integration_type: str) -> ActionResponse:
        """Remove an integration configuration.

        Args:
            integration_type: The integration type to remove.
        """
        data = await self._request("DELETE", f"/v1/integrations/{integration_type}")
        return ActionResponse.model_validate(data)

    async def test(self, integration_type: str) -> IntegrationTestResponse:
        """Send a test notification through the specified integration.

        Args:
            integration_type: The integration type to test.
        """
        data = await self._request("POST", f"/v1/integrations/{integration_type}/test")
        return IntegrationTestResponse.model_validate(data)
