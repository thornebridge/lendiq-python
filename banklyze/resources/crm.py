"""CRM resource — config, field mapping, sync, and test."""

from __future__ import annotations

from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.common import ActionResponse
from banklyze.types.crm import (
    CRMConfigResponse,
    FieldMappingResponse,
    SyncLogResponse,
    SyncTriggerResponse,
    ConnectionTestResponse,
)


class CrmResource(SyncAPIResource):

    def get_config(self, provider: str) -> CRMConfigResponse:
        """Get CRM configuration for a provider."""
        data = self._request("GET", f"/v1/crm/config/{provider}")
        return CRMConfigResponse.model_validate(data)

    def update_config(self, provider: str, **kwargs: Any) -> CRMConfigResponse:
        """Create or update CRM configuration for a provider."""
        data = self._request("PUT", f"/v1/crm/config/{provider}", json=kwargs)
        return CRMConfigResponse.model_validate(data)

    def delete_config(self, provider: str) -> ActionResponse:
        """Remove CRM configuration for a provider."""
        data = self._request("DELETE", f"/v1/crm/config/{provider}")
        return ActionResponse.model_validate(data)

    def test(self, provider: str) -> ConnectionTestResponse:
        """Test CRM connection for a provider."""
        data = self._request("POST", f"/v1/crm/config/{provider}/test")
        return ConnectionTestResponse.model_validate(data)

    def get_field_mapping(self, provider: str) -> FieldMappingResponse:
        """Get field mapping for a provider."""
        data = self._request("GET", f"/v1/crm/field-mapping/{provider}")
        return FieldMappingResponse.model_validate(data)

    def update_field_mapping(self, provider: str, **kwargs: Any) -> FieldMappingResponse:
        """Update field mapping for a provider."""
        data = self._request("PUT", f"/v1/crm/field-mapping/{provider}", json=kwargs)
        return FieldMappingResponse.model_validate(data)

    def sync(self, *, deal_id: int) -> SyncTriggerResponse:
        """Trigger a manual CRM sync for a deal."""
        data = self._request("POST", "/v1/crm/sync", json={"deal_id": deal_id})
        return SyncTriggerResponse.model_validate(data)

    def sync_log(self, *, page: int = 1, per_page: int = 25, deal_id: int | None = None) -> SyncLogResponse:
        """List CRM sync log entries."""
        data = self._request("GET", "/v1/crm/sync-log", params={"page": page, "per_page": per_page, "deal_id": deal_id})
        return SyncLogResponse.model_validate(data)


class AsyncCrmResource(AsyncAPIResource):

    async def get_config(self, provider: str) -> CRMConfigResponse:
        """Get CRM configuration for a provider."""
        data = await self._request("GET", f"/v1/crm/config/{provider}")
        return CRMConfigResponse.model_validate(data)

    async def update_config(self, provider: str, **kwargs: Any) -> CRMConfigResponse:
        """Create or update CRM configuration for a provider."""
        data = await self._request("PUT", f"/v1/crm/config/{provider}", json=kwargs)
        return CRMConfigResponse.model_validate(data)

    async def delete_config(self, provider: str) -> ActionResponse:
        """Remove CRM configuration for a provider."""
        data = await self._request("DELETE", f"/v1/crm/config/{provider}")
        return ActionResponse.model_validate(data)

    async def test(self, provider: str) -> ConnectionTestResponse:
        """Test CRM connection for a provider."""
        data = await self._request("POST", f"/v1/crm/config/{provider}/test")
        return ConnectionTestResponse.model_validate(data)

    async def get_field_mapping(self, provider: str) -> FieldMappingResponse:
        """Get field mapping for a provider."""
        data = await self._request("GET", f"/v1/crm/field-mapping/{provider}")
        return FieldMappingResponse.model_validate(data)

    async def update_field_mapping(self, provider: str, **kwargs: Any) -> FieldMappingResponse:
        """Update field mapping for a provider."""
        data = await self._request("PUT", f"/v1/crm/field-mapping/{provider}", json=kwargs)
        return FieldMappingResponse.model_validate(data)

    async def sync(self, *, deal_id: int) -> SyncTriggerResponse:
        """Trigger a manual CRM sync for a deal."""
        data = await self._request("POST", "/v1/crm/sync", json={"deal_id": deal_id})
        return SyncTriggerResponse.model_validate(data)

    async def sync_log(self, *, page: int = 1, per_page: int = 25, deal_id: int | None = None) -> SyncLogResponse:
        """List CRM sync log entries."""
        data = await self._request("GET", "/v1/crm/sync-log", params={"page": page, "per_page": per_page, "deal_id": deal_id})
        return SyncLogResponse.model_validate(data)
