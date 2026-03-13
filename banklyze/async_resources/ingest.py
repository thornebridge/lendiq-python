"""Async ingest resource — create CRM ingest batches and check batch status."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient


class AsyncIngestResource:
    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

    async def create(
        self,
        *,
        documents: list[dict[str, Any]],
        callback_url: str | None = None,
        external_reference: str | None = None,
    ) -> dict[str, Any]:
        """Create a new ingest batch.

        Args:
            documents: List of document descriptors, each with at least
                ``url`` and ``deal_external_reference`` keys.
            callback_url: Optional URL to call when the batch completes.
            external_reference: Optional external reference for the batch.

        Returns:
            Batch response with ``batch_id``, ``status``, and per-document details.
        """
        payload: dict[str, Any] = {"documents": documents}
        if callback_url:
            payload["callback_url"] = callback_url
        if external_reference:
            payload["external_reference"] = external_reference
        return await self._client._request("POST", "/v1/ingest", json=payload)

    async def get_batch(self, batch_id: int) -> dict[str, Any]:
        """Get the status of an ingest batch.

        Args:
            batch_id: The batch ID returned from ``create()``.

        Returns:
            Batch details including per-document statuses.
        """
        return await self._client._request("GET", f"/v1/ingest/{batch_id}")
