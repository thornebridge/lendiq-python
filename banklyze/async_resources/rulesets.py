"""Async rulesets resource — CRUD for underwriting rulesets."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient


class AsyncRulesetsResource:
    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

    async def list(self) -> dict[str, Any]:
        return await self._client._request("GET", "/v1/rulesets")

    async def create(self, **kwargs: Any) -> dict[str, Any]:
        return await self._client._request("POST", "/v1/rulesets", json=kwargs)

    async def get(self, ruleset_id: int) -> dict[str, Any]:
        return await self._client._request("GET", f"/v1/rulesets/{ruleset_id}")

    async def update(self, ruleset_id: int, **kwargs: Any) -> dict[str, Any]:
        return await self._client._request(
            "PUT", f"/v1/rulesets/{ruleset_id}", json=kwargs,
        )

    async def delete(self, ruleset_id: int) -> dict[str, Any]:
        return await self._client._request(
            "DELETE", f"/v1/rulesets/{ruleset_id}",
        )

    async def set_default(self, ruleset_id: int) -> dict[str, Any]:
        return await self._client._request(
            "POST", f"/v1/rulesets/{ruleset_id}/set-default",
        )
