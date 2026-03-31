"""Base classes for sync and async API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lendiq.async_client import AsyncLendIQClient
    from lendiq.client import LendIQClient


class SyncAPIResource:
    """Base class for synchronous resource implementations."""

    _client: LendIQClient

    def __init__(self, client: LendIQClient) -> None:
        self._client = client

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        return self._client._request(method, path, **kwargs)


class AsyncAPIResource:
    """Base class for asynchronous resource implementations."""

    _client: AsyncLendIQClient

    def __init__(self, client: AsyncLendIQClient) -> None:
        self._client = client

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        return await self._client._request(method, path, **kwargs)
