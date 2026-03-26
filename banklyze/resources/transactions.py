"""Transactions resource — list transactions by document or deal."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.transaction import (
    Transaction,
    TransactionCorrectionListResponse,
    TransactionDetail,
    TransactionListResponse,
)

if TYPE_CHECKING:
    from banklyze.pagination import AsyncPageIterator, PageIterator


class TransactionsResource(SyncAPIResource):
    def list_all_for_document(self, document_id: int, **filters: Any) -> PageIterator[Transaction]:
        """Iterate over all transactions for a document, auto-fetching pages.

        Usage::

            for txn in client.transactions.list_all_for_document(document_id=7):
                print(txn.date, txn.amount)
        """
        from banklyze.pagination import PageIterator

        return PageIterator(
            self._client,
            f"/v1/documents/{document_id}/transactions",
            model=Transaction,
            params=filters,
        )

    def list_all_for_deal(self, deal_id: int, **filters: Any) -> PageIterator[Transaction]:
        """Iterate over all transactions for a deal, auto-fetching pages.

        Usage::

            for txn in client.transactions.list_all_for_deal(deal_id=42):
                print(txn.date, txn.amount)
        """
        from banklyze.pagination import PageIterator

        return PageIterator(
            self._client,
            f"/v1/deals/{deal_id}/transactions",
            model=Transaction,
            params=filters,
        )

    def list_for_document(
        self,
        document_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
        type: str | None = None,
        flagged: bool | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> TransactionListResponse:
        data = self._request(
            "GET",
            f"/v1/documents/{document_id}/transactions",
            params={
                "page": page,
                "per_page": per_page,
                "type": type,
                "flagged": flagged,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        return TransactionListResponse.model_validate(data)

    def list_for_deal(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
        type: str | None = None,
        flagged: bool | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> TransactionListResponse:
        data = self._request(
            "GET",
            f"/v1/deals/{deal_id}/transactions",
            params={
                "page": page,
                "per_page": per_page,
                "type": type,
                "flagged": flagged,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        return TransactionListResponse.model_validate(data)

    def correct(
        self,
        document_id: int,
        transaction_id: int,
        **fields: Any,
    ) -> TransactionDetail:
        """Correct a transaction's categorization or amount."""
        data = self._request(
            "PATCH",
            f"/v1/documents/{document_id}/transactions/{transaction_id}",
            json=fields,
        )
        return TransactionDetail.model_validate(data)

    def corrections(self, transaction_id: int) -> TransactionCorrectionListResponse:
        """List correction history for a transaction."""
        data = self._request("GET", f"/v1/transactions/{transaction_id}/corrections")
        return TransactionCorrectionListResponse.model_validate(data)


class AsyncTransactionsResource(AsyncAPIResource):
    async def list_for_document(
        self,
        document_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
        type: str | None = None,
        flagged: bool | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> TransactionListResponse:
        data = await self._request(
            "GET",
            f"/v1/documents/{document_id}/transactions",
            params={
                "page": page,
                "per_page": per_page,
                "type": type,
                "flagged": flagged,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        return TransactionListResponse.model_validate(data)

    async def list_for_deal(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
        type: str | None = None,
        flagged: bool | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> TransactionListResponse:
        data = await self._request(
            "GET",
            f"/v1/deals/{deal_id}/transactions",
            params={
                "page": page,
                "per_page": per_page,
                "type": type,
                "flagged": flagged,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        return TransactionListResponse.model_validate(data)

    async def correct(
        self,
        document_id: int,
        transaction_id: int,
        **fields: Any,
    ) -> TransactionDetail:
        """Correct a transaction's categorization or amount."""
        data = await self._request(
            "PATCH",
            f"/v1/documents/{document_id}/transactions/{transaction_id}",
            json=fields,
        )
        return TransactionDetail.model_validate(data)

    async def corrections(self, transaction_id: int) -> TransactionCorrectionListResponse:
        """List correction history for a transaction."""
        data = await self._request("GET", f"/v1/transactions/{transaction_id}/corrections")
        return TransactionCorrectionListResponse.model_validate(data)

    def list_all_for_document(self, document_id: int, **filters: Any) -> AsyncPageIterator[Transaction]:
        """Iterate over all transactions for a document, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(
            self._client,
            f"/v1/documents/{document_id}/transactions",
            model=Transaction,
            params=filters,
        )

    def list_all_for_deal(self, deal_id: int, **filters: Any) -> AsyncPageIterator[Transaction]:
        """Iterate over all transactions for a deal, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(
            self._client,
            f"/v1/deals/{deal_id}/transactions",
            model=Transaction,
            params=filters,
        )
