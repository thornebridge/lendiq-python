"""Rulesets resource — CRUD for underwriting rulesets."""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse
from lendiq.types.ruleset import (
    Ruleset,
    RulesetListResponse,
)


class RulesetsResource(SyncAPIResource):
    def list(self) -> RulesetListResponse:
        data = self._request("GET", "/v1/rulesets")
        return RulesetListResponse.model_validate(data)

    def create(self, **kwargs: Any) -> Ruleset:
        data = self._request("POST", "/v1/rulesets", json=kwargs)
        return Ruleset.model_validate(data)

    def get(self, ruleset_id: int) -> Ruleset:
        data = self._request("GET", f"/v1/rulesets/{ruleset_id}")
        return Ruleset.model_validate(data)

    def update(self, ruleset_id: int, **kwargs: Any) -> Ruleset:
        data = self._request(
            "PUT", f"/v1/rulesets/{ruleset_id}", json=kwargs,
        )
        return Ruleset.model_validate(data)

    def delete(self, ruleset_id: int) -> ActionResponse:
        data = self._request(
            "DELETE", f"/v1/rulesets/{ruleset_id}",
        )
        return ActionResponse.model_validate(data)

    def set_default(self, ruleset_id: int) -> ActionResponse:
        data = self._request(
            "POST", f"/v1/rulesets/{ruleset_id}/set-default",
        )
        return ActionResponse.model_validate(data)


class AsyncRulesetsResource(AsyncAPIResource):
    async def list(self) -> RulesetListResponse:
        data = await self._request("GET", "/v1/rulesets")
        return RulesetListResponse.model_validate(data)

    async def create(self, **kwargs: Any) -> Ruleset:
        data = await self._request("POST", "/v1/rulesets", json=kwargs)
        return Ruleset.model_validate(data)

    async def get(self, ruleset_id: int) -> Ruleset:
        data = await self._request("GET", f"/v1/rulesets/{ruleset_id}")
        return Ruleset.model_validate(data)

    async def update(self, ruleset_id: int, **kwargs: Any) -> Ruleset:
        data = await self._request(
            "PUT", f"/v1/rulesets/{ruleset_id}", json=kwargs,
        )
        return Ruleset.model_validate(data)

    async def delete(self, ruleset_id: int) -> ActionResponse:
        data = await self._request(
            "DELETE", f"/v1/rulesets/{ruleset_id}",
        )
        return ActionResponse.model_validate(data)

    async def set_default(self, ruleset_id: int) -> ActionResponse:
        data = await self._request(
            "POST", f"/v1/rulesets/{ruleset_id}/set-default",
        )
        return ActionResponse.model_validate(data)
