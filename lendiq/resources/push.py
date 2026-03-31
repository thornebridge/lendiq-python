"""Push notifications resource — VAPID key, subscribe, unsubscribe."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.push import PushStatusResponse, VapidKeyResponse


class PushResource(SyncAPIResource):

    def vapid_key(self) -> VapidKeyResponse:
        """Get the VAPID public key for web push subscriptions."""
        data = self._request("GET", "/v1/push/vapid-key")
        return VapidKeyResponse.model_validate(data)

    def subscribe(self, **kwargs: Any) -> PushStatusResponse:
        """Register or update a push subscription for the authenticated user."""
        data = self._request("POST", "/v1/push/subscribe", json=kwargs)
        return PushStatusResponse.model_validate(data)

    def unsubscribe(self, **kwargs: Any) -> PushStatusResponse:
        """Remove a push subscription for the authenticated user."""
        data = self._request("DELETE", "/v1/push/subscribe", json=kwargs)
        return PushStatusResponse.model_validate(data)


class AsyncPushResource(AsyncAPIResource):

    async def vapid_key(self) -> VapidKeyResponse:
        """Get the VAPID public key for web push subscriptions."""
        data = await self._request("GET", "/v1/push/vapid-key")
        return VapidKeyResponse.model_validate(data)

    async def subscribe(self, **kwargs: Any) -> PushStatusResponse:
        """Register or update a push subscription for the authenticated user."""
        data = await self._request("POST", "/v1/push/subscribe", json=kwargs)
        return PushStatusResponse.model_validate(data)

    async def unsubscribe(self, **kwargs: Any) -> PushStatusResponse:
        """Remove a push subscription for the authenticated user."""
        data = await self._request("DELETE", "/v1/push/subscribe", json=kwargs)
        return PushStatusResponse.model_validate(data)
