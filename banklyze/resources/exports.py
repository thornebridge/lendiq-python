"""Exports resource — CSV and PDF report downloads."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class ExportsResource:
    def __init__(self, client: BanklyzeClient):
        self._client = client

    def deal_csv(self, deal_id: int) -> bytes:
        return self._client._request("GET", f"/v1/deals/{deal_id}/export/csv", raw=True)

    def deal_pdf(self, deal_id: int) -> bytes:
        return self._client._request("GET", f"/v1/deals/{deal_id}/export/pdf", raw=True)

    def document_csv(self, document_id: int) -> bytes:
        return self._client._request("GET", f"/v1/documents/{document_id}/export/csv", raw=True)

    def document_pdf(self, document_id: int) -> bytes:
        return self._client._request("GET", f"/v1/documents/{document_id}/pdf", raw=True)
