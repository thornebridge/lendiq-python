"""Webhooks resource — configure and test webhook delivery."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse
from lendiq.types.webhook import (
    WebhookConfig,
    WebhookDeliveryDetail,
    WebhookDeliveryListResponse,
    WebhookTestResult,
)


class WebhooksResource(SyncAPIResource):
    def get_config(self) -> WebhookConfig:
        data = self._request("GET", "/v1/webhooks/config")
        return WebhookConfig.model_validate(data)

    def update_config(
        self,
        *,
        url: str,
        secret: str | None = None,
        events: list[str] | None = None,
    ) -> WebhookConfig:
        body: dict[str, Any] = {"url": url}
        if secret is not None:
            body["secret"] = secret
        if events is not None:
            body["events"] = events
        data = self._request("PUT", "/v1/webhooks/config", json=body)
        return WebhookConfig.model_validate(data)

    def delete_config(self) -> ActionResponse:
        data = self._request("DELETE", "/v1/webhooks/config")
        return ActionResponse.model_validate(data)

    def test(self) -> WebhookTestResult:
        data = self._request("POST", "/v1/webhooks/test")
        return WebhookTestResult.model_validate(data)

    def list_deliveries(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
        event_type: str | None = None,
        success: bool | None = None,
    ) -> WebhookDeliveryListResponse:
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if event_type is not None:
            params["event_type"] = event_type
        if success is not None:
            params["success"] = str(success).lower()
        data = self._request("GET", "/v1/webhooks/deliveries", params=params)
        return WebhookDeliveryListResponse.model_validate(data)

    def get_delivery(self, delivery_id: int) -> WebhookDeliveryDetail:
        data = self._request("GET", f"/v1/webhooks/deliveries/{delivery_id}")
        return WebhookDeliveryDetail.model_validate(data)

    def retry_delivery(self, delivery_id: int) -> ActionResponse:
        data = self._request("POST", f"/v1/webhooks/deliveries/{delivery_id}/retry")
        return ActionResponse.model_validate(data)


class AsyncWebhooksResource(AsyncAPIResource):
    async def get_config(self) -> WebhookConfig:
        data = await self._request("GET", "/v1/webhooks/config")
        return WebhookConfig.model_validate(data)

    async def update_config(
        self,
        *,
        url: str,
        secret: str | None = None,
        events: list[str] | None = None,
    ) -> WebhookConfig:
        body: dict[str, Any] = {"url": url}
        if secret is not None:
            body["secret"] = secret
        if events is not None:
            body["events"] = events
        data = await self._request("PUT", "/v1/webhooks/config", json=body)
        return WebhookConfig.model_validate(data)

    async def delete_config(self) -> ActionResponse:
        data = await self._request("DELETE", "/v1/webhooks/config")
        return ActionResponse.model_validate(data)

    async def test(self) -> WebhookTestResult:
        data = await self._request("POST", "/v1/webhooks/test")
        return WebhookTestResult.model_validate(data)

    async def list_deliveries(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
        event_type: str | None = None,
        success: bool | None = None,
    ) -> WebhookDeliveryListResponse:
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if event_type is not None:
            params["event_type"] = event_type
        if success is not None:
            params["success"] = str(success).lower()
        data = await self._request("GET", "/v1/webhooks/deliveries", params=params)
        return WebhookDeliveryListResponse.model_validate(data)

    async def get_delivery(self, delivery_id: int) -> WebhookDeliveryDetail:
        data = await self._request("GET", f"/v1/webhooks/deliveries/{delivery_id}")
        return WebhookDeliveryDetail.model_validate(data)

    async def retry_delivery(self, delivery_id: int) -> ActionResponse:
        data = await self._request("POST", f"/v1/webhooks/deliveries/{delivery_id}/retry")
        return ActionResponse.model_validate(data)
