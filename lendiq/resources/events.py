"""Events resource — SSE streaming for deal pipeline progress."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator

if TYPE_CHECKING:
    from lendiq.async_client import AsyncLendIQClient
    from lendiq.client import LendIQClient


class SSEEvent:
    """A parsed Server-Sent Event."""

    __slots__ = ("id", "event", "data")

    def __init__(self, *, id: str | None = None, event: str = "message", data: str = ""):
        self.id = id
        self.event = event
        self.data = data

    def json(self) -> dict[str, Any]:
        """Parse the data field as JSON."""
        import json
        return json.loads(self.data)

    def __repr__(self) -> str:
        return f"SSEEvent(id={self.id!r}, event={self.event!r}, data={self.data[:80]!r})"


def _parse_sse_lines(lines: list[str]) -> SSEEvent | None:
    """Parse accumulated SSE lines into an event, or None if empty/comment-only."""
    event_id = None
    event_type = "message"
    data_parts: list[str] = []

    for line in lines:
        if line.startswith(":"):
            continue  # SSE comment
        if ":" in line:
            field, _, value = line.partition(":")
            value = value.lstrip(" ")  # SSE spec: strip single leading space
        else:
            field = line
            value = ""

        if field == "id":
            event_id = value
        elif field == "event":
            event_type = value
        elif field == "data":
            data_parts.append(value)

    if not data_parts:
        return None

    return SSEEvent(id=event_id, event=event_type, data="\n".join(data_parts))


class EventsResource:
    """Stream deal pipeline events via SSE."""

    def __init__(self, client: LendIQClient):
        self._client = client

    def stream(
        self,
        deal_id: int,
        *,
        document_id: int | None = None,
        last_event_id: int | None = None,
    ) -> Iterator[SSEEvent]:
        """Stream pipeline events for a deal.

        Yields SSEEvent objects as they arrive. The connection stays open
        until the server closes it or the iterator is abandoned.

        Usage::

            for event in client.events.stream(deal_id=42):
                if event.event == "stage":
                    payload = event.json()
                    print(f"Stage: {payload['stage']}")
        """
        params: dict[str, Any] = {}
        if document_id is not None:
            params["document_id"] = document_id
        if last_event_id is not None:
            params["last_event_id"] = last_event_id

        with self._client._http.stream(
            "GET",
            f"/v1/events/deals/{deal_id}",
            params={k: v for k, v in params.items() if v is not None},
        ) as response:
            response.raise_for_status()
            lines: list[str] = []
            for line in response.iter_lines():
                if line == "":
                    # Empty line = end of event
                    if lines:
                        evt = _parse_sse_lines(lines)
                        if evt is not None:
                            yield evt
                        lines = []
                else:
                    lines.append(line)
            # Handle any trailing lines
            if lines:
                evt = _parse_sse_lines(lines)
                if evt is not None:
                    yield evt

    def stream_org(self, *, last_event_id: int | None = None) -> Iterator[SSEEvent]:
        """Stream org-level business events (deal created, status changed, etc.)."""
        params: dict[str, Any] = {}
        if last_event_id is not None:
            params["last_event_id"] = last_event_id
        with self._client._http.stream(
            "GET", "/v1/events/org",
            params={k: v for k, v in params.items() if v is not None},
        ) as response:
            response.raise_for_status()
            lines: list[str] = []
            for line in response.iter_lines():
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

    def stream_batch(self, batch_id: str, *, last_event_id: int | None = None) -> Iterator[SSEEvent]:
        """Stream events for a CRM ingest batch."""
        params: dict[str, Any] = {}
        if last_event_id is not None:
            params["last_event_id"] = last_event_id
        with self._client._http.stream(
            "GET", f"/v1/events/batches/{batch_id}",
            params={k: v for k, v in params.items() if v is not None},
        ) as response:
            response.raise_for_status()
            lines: list[str] = []
            for line in response.iter_lines():
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


class AsyncEventsResource:
    """Stream deal pipeline events via SSE (async)."""

    def __init__(self, client: AsyncLendIQClient):
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

    async def stream_org(self, *, last_event_id: int | None = None) -> AsyncIterator[SSEEvent]:
        """Stream org-level business events (async)."""
        params: dict[str, Any] = {}
        if last_event_id is not None:
            params["last_event_id"] = last_event_id
        async with self._client._http.stream(
            "GET", "/v1/events/org",
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

    async def stream_batch(self, batch_id: str, *, last_event_id: int | None = None) -> AsyncIterator[SSEEvent]:
        """Stream events for a CRM ingest batch (async)."""
        params: dict[str, Any] = {}
        if last_event_id is not None:
            params["last_event_id"] = last_event_id
        async with self._client._http.stream(
            "GET", f"/v1/events/batches/{batch_id}",
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
