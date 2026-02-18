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

    def statement_csv(self, statement_id: int) -> bytes:
        return self._client._request("GET", f"/v1/statements/{statement_id}/export/csv", raw=True)

    def statement_pdf(self, statement_id: int) -> bytes:
        return self._client._request("GET", f"/v1/statements/{statement_id}/export/pdf", raw=True)
