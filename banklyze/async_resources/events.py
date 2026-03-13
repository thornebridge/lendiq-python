"""Async events resource — SSE streaming for deal pipeline progress."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient

from banklyze.resources.events import SSEEvent, _parse_sse_lines


class AsyncEventsResource:
    """Stream deal pipeline events via SSE (async)."""

    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

    async def stream(
        self,
        deal_id: int,
        *,
        document_id: int | None = None,
        last_event_id: int | None = None,
    ) -> AsyncIterator[SSEEvent]:
        """Async stream pipeline events for a deal.

        Usage::

            async for event in await client.events.stream(deal_id=42):
                if event.event == "stage":
                    payload = event.json()
                    print(f"Stage: {payload['stage']}")
        """
        params: dict[str, Any] = {}
        if document_id is not None:
            params["document_id"] = document_id
        if last_event_id is not None:
            params["last_event_id"] = last_event_id

        async with self._client._http.stream(
            "GET",
            f"/v1/events/deals/{deal_id}",
            params={k: v for k, v in params.items() if v is not None},
        ) as response:
            response.raise_for_status()
            lines: list[str] = []
            async for line in response.aiter_lines():
                if line == "":
                    if lines:
                        evt = _parse_sse_lines(lines)
                        if evt is not None:
                            yield evt
                        lines = []
                else:
                    lines.append(line)
            if lines:
                evt = _parse_sse_lines(lines)
                if evt is not None:
                    yield evt
