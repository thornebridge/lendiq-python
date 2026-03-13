"""Webhooks resource — configure and test webhook delivery."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class WebhooksResource:
    def __init__(self, client: BanklyzeClient):
        self._client = client

    def get_config(self) -> dict[str, Any]:
        return self._client._request("GET", "/v1/webhooks")

    def update_config(
        self,
        *,
        url: str,
        secret: str | None = None,
        events: list[str] | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"url": url}
        if secret is not None:
            body["secret"] = secret
        if events is not None:
            body["events"] = events
        return self._client._request("PUT", "/v1/webhooks", json=body)

    def delete_config(self) -> dict[str, Any]:
        return self._client._request("DELETE", "/v1/webhooks")

    def test(self) -> dict[str, Any]:
        return self._client._request("POST", "/v1/webhooks/test")

    def list_deliveries(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
        event_type: str | None = None,
        success: bool | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "per_page": per_page}
        if event_type is not None:
            params["event_type"] = event_type
        if success is not None:
            params["success"] = str(success).lower()
        return self._client._request("GET", "/v1/webhooks/deliveries", params=params)

    def get_delivery(self, delivery_id: int) -> dict[str, Any]:
        return self._client._request("GET", f"/v1/webhooks/deliveries/{delivery_id}")

    def retry_delivery(self, delivery_id: int) -> dict[str, Any]:
        return self._client._request("POST", f"/v1/webhooks/deliveries/{delivery_id}/retry")
