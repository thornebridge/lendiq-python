"""Async transactions resource — list transactions by document or deal."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient
    from banklyze.pagination import AsyncPageIterator


class AsyncTransactionsResource:
    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

    async def list_for_document(
        self,
        document_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        return await self._client._request(
            "GET",
            f"/v1/documents/{document_id}/transactions",
            params={"page": page, "per_page": per_page},
        )

    async def list_for_deal(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        return await self._client._request(
            "GET",
            f"/v1/deals/{deal_id}/transactions",
            params={"page": page, "per_page": per_page},
        )

    def list_all_for_document(self, document_id: int, **filters: Any) -> AsyncPageIterator:
        """Iterate over all transactions for a document, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(
            self._client,
            f"/v1/documents/{document_id}/transactions",
            data_key="transactions",
            params=filters,
        )

    def list_all_for_deal(self, deal_id: int, **filters: Any) -> AsyncPageIterator:
        """Iterate over all transactions for a deal, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(
            self._client,
            f"/v1/deals/{deal_id}/transactions",
            data_key="transactions",
            params=filters,
        )
