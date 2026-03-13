"""Auto-pagination iterators for list endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class PageIterator:
    """Lazily iterate over all items across paginated API responses.

    Usage::

        for deal in PageIterator(client, "/v1/deals", data_key="deals"):
            print(deal["business_name"])
    """

    def __init__(
        self,
        client: BanklyzeClient,
        path: str,
        *,
        data_key: str = "data",
        params: dict[str, Any] | None = None,
        per_page: int = 100,
    ):
        self._client = client
        self._path = path
        self._data_key = data_key
        self._params = dict(params or {})
        self._per_page = per_page
        self._page = 1

    def __iter__(self) -> Iterator[dict[str, Any]]:
        while True:
            request_params = {
                **self._params,
                "page": self._page,
                "per_page": self._per_page,
            }
            response = self._client._request("GET", self._path, params=request_params)

            items = response.get(self._data_key, [])
            yield from items

            # Determine total pages from pagination metadata
            pagination = response.get("pagination") or response.get("meta") or {}
            total_pages = pagination.get("total_pages", 1)

            if self._page >= total_pages or not items:
                break
            self._page += 1


class AsyncPageIterator:
    """Async variant of PageIterator for use with an async client.

    Usage::

        async for deal in AsyncPageIterator(client, "/v1/deals", data_key="deals"):
            print(deal["business_name"])
    """

    def __init__(
        self,
        client: Any,  # AsyncBanklyzeClient — avoided import for forward compat
        path: str,
        *,
        data_key: str = "data",
        params: dict[str, Any] | None = None,
        per_page: int = 100,
    ):
        self._client = client
        self._path = path
        self._data_key = data_key
        self._params = dict(params or {})
        self._per_page = per_page
        self._page = 1
        self._buffer: list[dict[str, Any]] = []
        self._exhausted = False

    def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        return self

    async def __anext__(self) -> dict[str, Any]:
        while not self._buffer:
            if self._exhausted:
                raise StopAsyncIteration

            request_params = {
                **self._params,
                "page": self._page,
                "per_page": self._per_page,
            }
            response = await self._client._request(
                "GET", self._path, params=request_params
            )

            items = response.get(self._data_key, [])
            pagination = response.get("pagination") or response.get("meta") or {}
            total_pages = pagination.get("total_pages", 1)

            if not items:
                raise StopAsyncIteration

            self._buffer = list(items)

            if self._page >= total_pages:
                self._exhausted = True
            else:
                self._page += 1

        return self._buffer.pop(0)
