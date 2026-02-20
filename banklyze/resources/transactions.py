"""Transactions resource — list transactions by document or deal."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class TransactionsResource:
    def __init__(self, client: BanklyzeClient):
        self._client = client

    def list_for_document(
        self,
        document_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        return self._client._request(
            "GET",
            f"/v1/documents/{document_id}/transactions",
            params={"page": page, "per_page": per_page},
        )

    def list_for_deal(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        return self._client._request(
            "GET",
            f"/v1/deals/{deal_id}/transactions",
            params={"page": page, "per_page": per_page},
        )
