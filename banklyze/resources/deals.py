"""Deals resource — CRUD, decision, notes, recommendation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class DealsResource:
    def __init__(self, client: BanklyzeClient):
        self._client = client

    def list(
        self,
        *,
        status: str | None = None,
        search: str | None = None,
        sort: str | None = None,
        page: int = 1,
        per_page: int = 25,
    ) -> dict[str, Any]:
        return self._client._request(
            "GET",
            "/v1/deals",
            params={"status": status, "search": search, "sort": sort, "page": page, "per_page": per_page},
        )

    def create(
        self,
        *,
        business_name: str,
        dba_name: str | None = None,
        owner_name: str | None = None,
        industry: str | None = None,
        funding_amount_requested: float | None = None,
        notes: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        body = {"business_name": business_name}
        if dba_name is not None:
            body["dba_name"] = dba_name
        if owner_name is not None:
            body["owner_name"] = owner_name
        if industry is not None:
            body["industry"] = industry
        if funding_amount_requested is not None:
            body["funding_amount_requested"] = funding_amount_requested
        if notes is not None:
            body["notes"] = notes
        return self._client._request("POST", "/v1/deals", json=body, headers=headers or None)

    def get(self, deal_id: int) -> dict[str, Any]:
        return self._client._request("GET", f"/v1/deals/{deal_id}")

    def update(self, deal_id: int, **fields) -> dict[str, Any]:
        return self._client._request("PATCH", f"/v1/deals/{deal_id}", json=fields)

    def delete(self, deal_id: int) -> dict[str, Any]:
        return self._client._request("DELETE", f"/v1/deals/{deal_id}")

    def decision(self, deal_id: int, *, decision: str, idempotency_key: str | None = None) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/decision",
            json={"decision": decision},
            headers=headers or None,
        )

    def notes(self, deal_id: int, *, page: int = 1, per_page: int = 25) -> dict[str, Any]:
        return self._client._request(
            "GET",
            f"/v1/deals/{deal_id}/notes",
            params={"page": page, "per_page": per_page},
        )

    def add_note(
        self,
        deal_id: int,
        *,
        content: str,
        author: str = "API",
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/notes",
            json={"content": content, "author": author},
            headers=headers or None,
        )

    def recommendation(self, deal_id: int) -> dict[str, Any]:
        return self._client._request("GET", f"/v1/deals/{deal_id}/recommendation")

    def regenerate_summary(self, deal_id: int, *, idempotency_key: str | None = None) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/regenerate-summary",
            headers=headers or None,
        )
