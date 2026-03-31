"""Ingest resource — create CRM ingest batches and check batch status."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.ingest import BatchStatusResponse, IngestResponse


class IngestResource(SyncAPIResource):
    def create(
        self,
        *,
        file_paths: list[str | Path],
        metadata: dict[str, Any],
        document_type: str | None = None,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> IngestResponse:
        """Create a new ingest batch with file uploads.

        Args:
            file_paths: List of local file paths to upload.
            metadata: Dict with deal-matching info (``external_reference``,
                ``business_name``, ``deal_id``, ``callback_url``, etc.).
                Sent as a JSON string in the ``metadata`` form field.
            document_type: Optional document type override for all files.
            idempotency_key: Optional idempotency key.
            gemini_model: Optional Gemini model override for extraction.

        Returns:
            Batch response with ``batch_id``, ``status``, and per-document details.
        """
        files = []
        handles = []
        try:
            for fp in file_paths:
                p = Path(fp)
                f = open(p, "rb")  # noqa: SIM115
                handles.append(f)
                files.append(("files", (p.name, f, "application/pdf")))

            params: dict[str, str] | None = None
            if document_type:
                params = {"document_type": document_type}

            headers: dict[str, str] = {}
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key
            if gemini_model:
                headers["X-Gemini-Model"] = gemini_model

            data = self._request(
                "POST",
                "/v1/ingest",
                files=files,
                params=params,
                headers=headers or None,
                timeout=self._client.TIMEOUT_UPLOAD,
                data={"metadata": json.dumps(metadata)},
            )
        finally:
            for f in handles:
                f.close()
        return IngestResponse.model_validate(data)

    def get_batch(self, batch_id: int) -> BatchStatusResponse:
        """Get the status of an ingest batch.

        Args:
            batch_id: The batch ID returned from ``create()``.

        Returns:
            Batch details including per-document statuses.
        """
        data = self._request("GET", f"/v1/ingest/{batch_id}")
        return BatchStatusResponse.model_validate(data)


class AsyncIngestResource(AsyncAPIResource):
    async def create(
        self,
        *,
        file_paths: list[str | Path],
        metadata: dict[str, Any],
        document_type: str | None = None,
        idempotency_key: str | None = None,
        gemini_model: str | None = None,
    ) -> IngestResponse:
        """Create a new ingest batch with file uploads.

        Args:
            file_paths: List of local file paths to upload.
            metadata: Dict with deal-matching info (``external_reference``,
                ``business_name``, ``deal_id``, ``callback_url``, etc.).
                Sent as a JSON string in the ``metadata`` form field.
            document_type: Optional document type override for all files.
            idempotency_key: Optional idempotency key.
            gemini_model: Optional Gemini model override for extraction.

        Returns:
            Batch response with ``batch_id``, ``status``, and per-document details.
        """
        files = []
        handles = []
        try:
            for fp in file_paths:
                p = Path(fp)
                f = open(p, "rb")  # noqa: SIM115
                handles.append(f)
                files.append(("files", (p.name, f, "application/pdf")))

            params: dict[str, str] | None = None
            if document_type:
                params = {"document_type": document_type}

            headers: dict[str, str] = {}
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key
            if gemini_model:
                headers["X-Gemini-Model"] = gemini_model

            data = await self._request(
                "POST",
                "/v1/ingest",
                files=files,
                params=params,
                headers=headers or None,
                timeout=self._client.TIMEOUT_UPLOAD,
                data={"metadata": json.dumps(metadata)},
            )
        finally:
            for f in handles:
                f.close()
        return IngestResponse.model_validate(data)

    async def get_batch(self, batch_id: int) -> BatchStatusResponse:
        """Get the status of an ingest batch.

        Args:
            batch_id: The batch ID returned from ``create()``.

        Returns:
            Batch details including per-document statuses.
        """
        data = await self._request("GET", f"/v1/ingest/{batch_id}")
        return BatchStatusResponse.model_validate(data)
