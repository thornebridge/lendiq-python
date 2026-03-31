"""Auto-pagination iterators for list endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Generic, Iterator, TypeVar, overload

from pydantic import BaseModel

if TYPE_CHECKING:
    from lendiq.client import LendIQClient

T = TypeVar("T")


class PageIterator(Generic[T]):
    """Lazily iterate over all items across paginated API responses.

    When *model* is provided, each item is validated into that Pydantic model::

        for deal in PageIterator(client, "/v1/deals", model=DealSummary):
            print(deal.business_name)  # typed!

    Without *model*, raw dicts are yielded (backward-compatible)::

        for deal in PageIterator(client, "/v1/deals"):
            print(deal["business_name"])
    """

    @overload
    def __init__(
        self,
        client: LendIQClient,
        path: str,
        *,
        model: type[T],
        data_key: str = ...,
        params: dict[str, Any] | None = ...,
        per_page: int = ...,
    ) -> None: ...

    @overload
    def __init__(
        self,
        client: LendIQClient,
        path: str,
        *,
        data_key: str = ...,
        params: dict[str, Any] | None = ...,
        per_page: int = ...,
    ) -> None: ...

    def __init__(
        self,
        client: LendIQClient,
        path: str,
        *,
        model: type[T] | None = None,
        data_key: str = "data",
        params: dict[str, Any] | None = None,
        per_page: int = 100,
    ):
        self._client = client
        self._path = path
        self._model = model
        self._data_key = data_key
        self._params = dict(params or {})
        self._per_page = per_page
        self._page = 1

    def __iter__(self) -> Iterator[T]:
        while True:
            request_params = {
                **self._params,
                "page": self._page,
                "per_page": self._per_page,
            }
            response = self._client._request("GET", self._path, params=request_params)

            items = response.get(self._data_key, [])
            for item in items:
                if self._model is not None and issubclass(self._model, BaseModel):
                    yield self._model.model_validate(item)  # type: ignore[misc]
                else:
                    yield item  # type: ignore[misc]

            # Determine total pages from pagination metadata
            meta = response.get("meta") or {}
            total_pages = meta.get("total_pages", 1)

            if self._page >= total_pages or not items:
                break
            self._page += 1


class AsyncPageIterator(Generic[T]):
    """Async variant of PageIterator for use with an async client.

    Usage::

        async for deal in AsyncPageIterator(client, "/v1/deals", model=DealSummary):
            print(deal.business_name)
    """

    @overload
    def __init__(
        self,
        client: Any,
        path: str,
        *,
        model: type[T],
        data_key: str = ...,
        params: dict[str, Any] | None = ...,
        per_page: int = ...,
    ) -> None: ...

    @overload
    def __init__(
        self,
        client: Any,
        path: str,
        *,
        data_key: str = ...,
        params: dict[str, Any] | None = ...,
        per_page: int = ...,
    ) -> None: ...

    def __init__(
        self,
        client: Any,  # AsyncLendIQClient — avoided import for forward compat
        path: str,
        *,
        model: type[T] | None = None,
        data_key: str = "data",
        params: dict[str, Any] | None = None,
        per_page: int = 100,
    ):
        self._client = client
        self._path = path
        self._model = model
        self._data_key = data_key
        self._params = dict(params or {})
        self._per_page = per_page
        self._page = 1
        self._buffer: list[T] = []
        self._exhausted = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
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
            meta = response.get("meta") or {}
            total_pages = meta.get("total_pages", 1)

            if not items:
                raise StopAsyncIteration

            if self._model is not None and issubclass(self._model, BaseModel):
                self._buffer = [self._model.model_validate(item) for item in items]  # type: ignore[misc]
            else:
                self._buffer = list(items)  # type: ignore[misc]

            if self._page >= total_pages:
                self._exhausted = True
            else:
                self._page += 1

        return self._buffer.pop(0)
