"""Exports resource — CSV and PDF report downloads."""

from __future__ import annotations

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource


class ExportsResource(SyncAPIResource):
    def deal_csv(self, deal_id: int) -> bytes:
        return self._request("GET", f"/v1/deals/{deal_id}/export/csv", raw=True)

    def deal_pdf(self, deal_id: int) -> bytes:
        return self._request(
            "GET", f"/v1/deals/{deal_id}/export/pdf", raw=True,
            timeout=self._client.TIMEOUT_REPORT,
        )

    def document_csv(self, document_id: int) -> bytes:
        return self._request("GET", f"/v1/documents/{document_id}/export/csv", raw=True)

    def document_pdf(self, document_id: int) -> bytes:
        return self._request(
            "GET", f"/v1/documents/{document_id}/pdf", raw=True,
            timeout=self._client.TIMEOUT_REPORT,
        )


class AsyncExportsResource(AsyncAPIResource):
    async def deal_csv(self, deal_id: int) -> bytes:
        return await self._request("GET", f"/v1/deals/{deal_id}/export/csv", raw=True)

    async def deal_pdf(self, deal_id: int) -> bytes:
        return await self._request(
            "GET", f"/v1/deals/{deal_id}/export/pdf", raw=True,
            timeout=self._client.TIMEOUT_REPORT,
        )

    async def document_csv(self, document_id: int) -> bytes:
        return await self._request(
            "GET", f"/v1/documents/{document_id}/export/csv", raw=True,
        )

    async def document_pdf(self, document_id: int) -> bytes:
        return await self._request(
            "GET", f"/v1/documents/{document_id}/pdf", raw=True,
            timeout=self._client.TIMEOUT_REPORT,
        )
