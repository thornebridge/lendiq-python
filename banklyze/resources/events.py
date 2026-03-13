"""Events resource — SSE streaming for deal pipeline progress."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterator

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


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

    def __init__(self, client: BanklyzeClient):
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
