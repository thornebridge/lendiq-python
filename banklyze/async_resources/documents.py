"""Async documents resource — upload, bulk upload, list, detail, status, reprocess, cancel."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient
    from banklyze.pagination import AsyncPageIterator


class AsyncDocumentsResource:
    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

    async def upload(
        self,
        deal_id: int,
        file_path: str | Path,
        *,
        document_type: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        p = Path(file_path)
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        params = {}
        if document_type:
            params["document_type"] = document_type
        with open(p, "rb") as f:
            return await self._client._request(
                "POST",
                f"/v1/deals/{deal_id}/documents",
                files={"file": (p.name, f, "application/pdf")},
                params=params or None,
                headers=headers or None,
            )

    async def upload_bulk(
        self,
        deal_id: int,
        file_paths: list[str | Path],
        *,
        document_type: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        params = {}
        if document_type:
            params["document_type"] = document_type
        files = []
        handles = []
        try:
            for fp in file_paths:
                p = Path(fp)
                f = open(p, "rb")
                handles.append(f)
                files.append(("files", (p.name, f, "application/pdf")))
            return await self._client._request(
                "POST",
                f"/v1/deals/{deal_id}/documents/bulk",
                files=files,
                params=params or None,
                headers=headers or None,
            )
        finally:
            for f in handles:
                f.close()

    async def list(self, deal_id: int, *, page: int = 1, per_page: int = 25) -> dict[str, Any]:
        return await self._client._request(
            "GET",
            f"/v1/deals/{deal_id}/documents",
            params={"page": page, "per_page": per_page},
        )

    async def get(self, document_id: int) -> dict[str, Any]:
        return await self._client._request("GET", f"/v1/documents/{document_id}")

    async def status(self, document_id: int) -> dict[str, Any]:
        return await self._client._request("GET", f"/v1/documents/{document_id}/status")

    async def reprocess(
        self, document_id: int, *, idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return await self._client._request(
            "POST",
            f"/v1/documents/{document_id}/reprocess",
            headers=headers or None,
        )

    async def cancel(
        self, document_id: int, *, idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return await self._client._request(
            "POST",
            f"/v1/documents/{document_id}/cancel",
            headers=headers or None,
        )

    async def reclassify(
        self,
        document_id: int,
        document_type: str,
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return await self._client._request(
            "POST",
            f"/v1/documents/{document_id}/reclassify",
            params={"document_type": document_type},
            headers=headers or None,
        )

    def list_all(self, deal_id: int, **filters: Any) -> AsyncPageIterator:
        """Iterate over all documents for a deal, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(
            self._client, f"/v1/deals/{deal_id}/documents", data_key="documents", params=filters,
        )
