"""Async exports resource — CSV and PDF report downloads."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient


class AsyncExportsResource:
    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

    async def deal_csv(self, deal_id: int) -> bytes:
        return await self._client._request("GET", f"/v1/deals/{deal_id}/export/csv", raw=True)

    async def deal_pdf(self, deal_id: int) -> bytes:
        return await self._client._request("GET", f"/v1/deals/{deal_id}/export/pdf", raw=True)

    async def document_csv(self, document_id: int) -> bytes:
        return await self._client._request(
            "GET", f"/v1/documents/{document_id}/export/csv", raw=True,
        )

    async def document_pdf(self, document_id: int) -> bytes:
        return await self._client._request("GET", f"/v1/documents/{document_id}/pdf", raw=True)
