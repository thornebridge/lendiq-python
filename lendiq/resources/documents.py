"""Documents resource — upload, bulk upload, list, detail, status, reprocess, cancel.

Contains both sync (``DocumentsResource``) and async (``AsyncDocumentsResource``)
implementations.  All methods return typed Pydantic models from
``lendiq.types.document``.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.triage import TriageResponse
from lendiq.types.document import (
    BatchDocumentStatusResponse,
    BulkUploadResponse,
    DocumentDetail,
    DocumentListResponse,
    DocumentStatusResponse,
    DocumentSummary,
    DocumentUploadResponse,
)

if TYPE_CHECKING:
    from lendiq.pagination import AsyncPageIterator, PageIterator


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _idempotency_headers(key: str | None) -> dict[str, str] | None:
    if key:
        return {"Idempotency-Key": key}
    return None


def _upload_params(document_type: str | None) -> dict[str, str] | None:
    if document_type:
        return {"document_type": document_type}
    return None


def _gemini_model_headers(
    gemini_model: str | None,
    extra: dict[str, str] | None = None,
) -> dict[str, str] | None:
    """Build headers dict, merging optional Gemini model override with extras."""
    headers: dict[str, str] = dict(extra) if extra else {}
    if gemini_model:
        headers["X-Gemini-Model"] = gemini_model
    return headers or None


# ---------------------------------------------------------------------------
# Sync resource
# ---------------------------------------------------------------------------


class DocumentsResource(SyncAPIResource):
    """Synchronous documents resource."""

    def upload(
        self,
        deal_id: int,
        file_path: str | Path,
        *,
        document_type: str | None = None,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> DocumentUploadResponse:
        p = Path(file_path)
        with open(p, "rb") as f:
            raw = self._request(
                "POST",
                f"/v1/deals/{deal_id}/documents",
                files={"file": (p.name, f, "application/pdf")},
                params=_upload_params(document_type),
                headers=_gemini_model_headers(gemini_model, _idempotency_headers(idempotency_key)),
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        return DocumentUploadResponse.model_validate(raw)

    def upload_bulk(
        self,
        deal_id: int,
        file_paths: list[str | Path],
        *,
        document_type: str | None = None,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> BulkUploadResponse:
        files = []
        handles = []
        try:
            for fp in file_paths:
                p = Path(fp)
                f = open(p, "rb")  # noqa: SIM115
                handles.append(f)
                files.append(("files", (p.name, f, "application/pdf")))
            raw = self._request(
                "POST",
                f"/v1/deals/{deal_id}/documents/bulk",
                files=files,
                params=_upload_params(document_type),
                headers=_gemini_model_headers(gemini_model, _idempotency_headers(idempotency_key)),
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        finally:
            for f in handles:
                f.close()
        return BulkUploadResponse.model_validate(raw)

    def list(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 25,
    ) -> DocumentListResponse:
        raw = self._request(
            "GET",
            f"/v1/deals/{deal_id}/documents",
            params={"page": page, "per_page": per_page},
        )
        return DocumentListResponse.model_validate(raw)

    def list_all(self, deal_id: int, **filters: Any) -> PageIterator[DocumentSummary]:
        """Iterate over all documents for a deal, auto-fetching pages.

        Usage::

            for doc in client.documents.list_all(deal_id=42):
                print(doc.id, doc.document_type)
        """
        from lendiq.pagination import PageIterator

        return PageIterator(
            self._client,
            f"/v1/deals/{deal_id}/documents",
            model=DocumentSummary,
            params=filters,
        )

    def get(self, document_id: int) -> DocumentDetail:
        raw = self._request("GET", f"/v1/documents/{document_id}")
        return DocumentDetail.model_validate(raw)

    def status(self, document_id: int) -> DocumentStatusResponse:
        raw = self._request("GET", f"/v1/documents/{document_id}/status")
        return DocumentStatusResponse.model_validate(raw)

    def reprocess(
        self,
        document_id: int,
        *,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> DocumentStatusResponse:
        raw = self._request(
            "POST",
            f"/v1/documents/{document_id}/reprocess",
            headers=_gemini_model_headers(gemini_model, _idempotency_headers(idempotency_key)),
        )
        return DocumentStatusResponse.model_validate(raw)

    def cancel(
        self,
        document_id: int,
        *,
        idempotency_key: str | None = None,
    ) -> DocumentStatusResponse:
        raw = self._request(
            "POST",
            f"/v1/documents/{document_id}/cancel",
            headers=_idempotency_headers(idempotency_key),
        )
        return DocumentStatusResponse.model_validate(raw)

    def reclassify(
        self,
        document_id: int,
        document_type: str,
        *,
        idempotency_key: str | None = None,
    ) -> DocumentStatusResponse:
        raw = self._request(
            "POST",
            f"/v1/documents/{document_id}/reclassify",
            params={"document_type": document_type},
            headers=_idempotency_headers(idempotency_key),
        )
        return DocumentStatusResponse.model_validate(raw)

    def batch_status(self, document_ids: list[int]) -> BatchDocumentStatusResponse:
        """Check processing status for multiple documents at once."""
        raw = self._request(
            "POST",
            "/v1/documents/batch-status",
            json={"document_ids": document_ids},
        )
        return BatchDocumentStatusResponse.model_validate(raw)

    def triage(
        self,
        file_path: str | Path,
        *,
        vision_fallback: bool = False,
    ) -> TriageResponse:
        """Triage a PDF — classify, assess quality, check integrity.

        Pre-processing analysis without full pipeline execution.

        Args:
            file_path: Path to the PDF file.
            vision_fallback: Use vision LLM fallback for classification.
        """
        p = Path(file_path)
        params: dict[str, Any] = {}
        if vision_fallback:
            params["vision_fallback"] = True
        with open(p, "rb") as f:
            raw = self._request(
                "POST",
                "/v1/documents/triage",
                files={"file": (p.name, f, "application/pdf")},
                params=params or None,
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        return TriageResponse.model_validate(raw)


# ---------------------------------------------------------------------------
# Async resource
# ---------------------------------------------------------------------------


class AsyncDocumentsResource(AsyncAPIResource):
    """Asynchronous documents resource."""

    async def upload(
        self,
        deal_id: int,
        file_path: str | Path,
        *,
        document_type: str | None = None,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> DocumentUploadResponse:
        p = Path(file_path)
        with open(p, "rb") as f:
            raw = await self._request(
                "POST",
                f"/v1/deals/{deal_id}/documents",
                files={"file": (p.name, f, "application/pdf")},
                params=_upload_params(document_type),
                headers=_gemini_model_headers(gemini_model, _idempotency_headers(idempotency_key)),
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        return DocumentUploadResponse.model_validate(raw)

    async def upload_bulk(
        self,
        deal_id: int,
        file_paths: list[str | Path],
        *,
        document_type: str | None = None,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> BulkUploadResponse:
        files = []
        handles = []
        try:
            for fp in file_paths:
                p = Path(fp)
                f = open(p, "rb")  # noqa: SIM115
                handles.append(f)
                files.append(("files", (p.name, f, "application/pdf")))
            raw = await self._request(
                "POST",
                f"/v1/deals/{deal_id}/documents/bulk",
                files=files,
                params=_upload_params(document_type),
                headers=_gemini_model_headers(gemini_model, _idempotency_headers(idempotency_key)),
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        finally:
            for f in handles:
                f.close()
        return BulkUploadResponse.model_validate(raw)

    async def list(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 25,
    ) -> DocumentListResponse:
        raw = await self._request(
            "GET",
            f"/v1/deals/{deal_id}/documents",
            params={"page": page, "per_page": per_page},
        )
        return DocumentListResponse.model_validate(raw)

    def list_all(self, deal_id: int, **filters: Any) -> AsyncPageIterator[DocumentSummary]:
        """Iterate over all documents for a deal, auto-fetching pages."""
        from lendiq.pagination import AsyncPageIterator

        return AsyncPageIterator(
            self._client,
            f"/v1/deals/{deal_id}/documents",
            model=DocumentSummary,
            params=filters,
        )

    async def get(self, document_id: int) -> DocumentDetail:
        raw = await self._request("GET", f"/v1/documents/{document_id}")
        return DocumentDetail.model_validate(raw)

    async def status(self, document_id: int) -> DocumentStatusResponse:
        raw = await self._request("GET", f"/v1/documents/{document_id}/status")
        return DocumentStatusResponse.model_validate(raw)

    async def reprocess(
        self,
        document_id: int,
        *,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> DocumentStatusResponse:
        raw = await self._request(
            "POST",
            f"/v1/documents/{document_id}/reprocess",
            headers=_gemini_model_headers(gemini_model, _idempotency_headers(idempotency_key)),
        )
        return DocumentStatusResponse.model_validate(raw)

    async def cancel(
        self,
        document_id: int,
        *,
        idempotency_key: str | None = None,
    ) -> DocumentStatusResponse:
        raw = await self._request(
            "POST",
            f"/v1/documents/{document_id}/cancel",
            headers=_idempotency_headers(idempotency_key),
        )
        return DocumentStatusResponse.model_validate(raw)

    async def reclassify(
        self,
        document_id: int,
        document_type: str,
        *,
        idempotency_key: str | None = None,
    ) -> DocumentStatusResponse:
        raw = await self._request(
            "POST",
            f"/v1/documents/{document_id}/reclassify",
            params={"document_type": document_type},
            headers=_idempotency_headers(idempotency_key),
        )
        return DocumentStatusResponse.model_validate(raw)

    async def batch_status(self, document_ids: list[int]) -> BatchDocumentStatusResponse:
        """Check processing status for multiple documents at once."""
        raw = await self._request(
            "POST",
            "/v1/documents/batch-status",
            json={"document_ids": document_ids},
        )
        return BatchDocumentStatusResponse.model_validate(raw)

    async def triage(
        self,
        file_path: str | Path,
        *,
        vision_fallback: bool = False,
    ) -> TriageResponse:
        """Triage a PDF — classify, assess quality, check integrity."""
        p = Path(file_path)
        params: dict[str, Any] = {}
        if vision_fallback:
            params["vision_fallback"] = True
        with open(p, "rb") as f:
            raw = await self._request(
                "POST",
                "/v1/documents/triage",
                files={"file": (p.name, f, "application/pdf")},
                params=params or None,
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        return TriageResponse.model_validate(raw)
