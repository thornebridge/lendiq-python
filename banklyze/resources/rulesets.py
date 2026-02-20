"""Rulesets resource — CRUD for underwriting rulesets."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class RulesetsResource:
    def __init__(self, client: BanklyzeClient):
        self._client = client

    def list(self) -> dict[str, Any]:
        return self._client._request("GET", "/v1/rulesets")

    def create(self, **kwargs: Any) -> dict[str, Any]:
        return self._client._request("POST", "/v1/rulesets", json=kwargs)

    def get(self, ruleset_id: int) -> dict[str, Any]:
        return self._client._request("GET", f"/v1/rulesets/{ruleset_id}")

    def update(self, ruleset_id: int, **kwargs: Any) -> dict[str, Any]:
        return self._client._request(
            "PUT", f"/v1/rulesets/{ruleset_id}", json=kwargs,
        )

    def delete(self, ruleset_id: int) -> dict[str, Any]:
        return self._client._request(
            "DELETE", f"/v1/rulesets/{ruleset_id}",
        )

    def set_default(self, ruleset_id: int) -> dict[str, Any]:
        return self._client._request(
            "POST", f"/v1/rulesets/{ruleset_id}/set-default",
        )
