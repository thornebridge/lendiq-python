"""AsyncBanklyzeClient — async variant of the Banklyze API client."""

from __future__ import annotations

import asyncio
import uuid
from typing import Any

import httpx

from banklyze._base import ClientConfig
from banklyze.async_resources.deals import AsyncDealsResource
from banklyze.async_resources.documents import AsyncDocumentsResource
from banklyze.async_resources.events import AsyncEventsResource
from banklyze.async_resources.exports import AsyncExportsResource
from banklyze.async_resources.ingest import AsyncIngestResource
from banklyze.async_resources.rulesets import AsyncRulesetsResource
from banklyze.async_resources.transactions import AsyncTransactionsResource
from banklyze.async_resources.webhooks import AsyncWebhooksResource
from banklyze.exceptions import (
    AuthenticationError,
    BanklyzeError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


class AsyncBanklyzeClient:
    """Async Banklyze API client.

    Usage::

        async with AsyncBanklyzeClient(api_key="bk_live_...") as client:
            deals = await client.deals.list()
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.banklyze.com",
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_backoff: float = 0.5,
        retry_max_backoff: float = 30.0,
    ):
        self._config = ClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            retry_max_backoff=retry_max_backoff,
        )
        self._http = httpx.AsyncClient(
            base_url=self._config.base_url,
            headers=self._config._build_headers(),
            timeout=timeout,
        )

        self.deals = AsyncDealsResource(self)
        self.documents = AsyncDocumentsResource(self)
        self.events = AsyncEventsResource(self)
        self.transactions = AsyncTransactionsResource(self)
        self.exports = AsyncExportsResource(self)
        self.ingest = AsyncIngestResource(self)
        self.rulesets = AsyncRulesetsResource(self)
        self.webhooks = AsyncWebhooksResource(self)

    @property
    def last_request_id(self) -> str | None:
        return self._config.last_request_id

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self) -> None:
        await self._http.aclose()

    # ── Internal request helpers ─────────────────────────────────────────────

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
        raw: bool = False,
    ) -> Any:
        """Make an async API request and return parsed JSON (or raw bytes if raw=True).

        Automatically retries on transient failures with exponential backoff.
        For mutating methods (POST/PATCH/PUT), only connection-level errors are
        retried (the request never reached the server). For idempotent methods
        (GET/DELETE/HEAD/OPTIONS), retryable HTTP status codes (429, 5xx) are
        also retried.
        """
        req_headers = dict(headers or {})
        req_headers["X-Request-ID"] = str(uuid.uuid4())

        last_exc: Exception | None = None
        last_resp: httpx.Response | None = None

        for attempt in range(1 + self._config.max_retries):
            try:
                resp = await self._http.request(
                    method,
                    path,
                    json=json,
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    files=files,
                    headers=req_headers,
                )

                # Capture the server-echoed request ID for debugging correlation
                self._config.last_request_id = resp.headers.get(
                    "X-Request-ID", req_headers["X-Request-ID"]
                )
                last_resp = resp

                if resp.status_code < 400:
                    if raw:
                        return resp.content
                    if resp.status_code == 204:
                        return {}
                    return resp.json()

                # Determine if this error is retryable
                if not self._config._should_retry(method, resp.status_code, attempt):
                    self._raise_for_status(resp)

                # For 429, honor Retry-After header
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after:
                        try:
                            delay = float(retry_after)
                        except ValueError:
                            delay = self._config._backoff_delay(attempt)
                    else:
                        delay = self._config._backoff_delay(attempt)
                else:
                    delay = self._config._backoff_delay(attempt)

                await asyncio.sleep(delay)
                last_exc = BanklyzeError(
                    f"HTTP {resp.status_code}",
                    status_code=resp.status_code,
                    request_id=self._config.last_request_id,
                )

            except (
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.WriteTimeout,
                httpx.PoolTimeout,
            ) as e:
                # Connection-level errors are always retryable (never reached server)
                self._config.last_request_id = req_headers.get("X-Request-ID")
                last_exc = e
                if attempt >= self._config.max_retries:
                    raise BanklyzeError(
                        f"Connection error after {attempt + 1} attempts: {e}",
                        request_id=self._config.last_request_id,
                    ) from e
                await asyncio.sleep(self._config._backoff_delay(attempt))

        # Exhausted retries — raise the last error
        if last_resp is not None:
            self._raise_for_status(last_resp)

        # Fallback: should not be reached, but guard against it
        if last_exc is not None:
            raise last_exc  # type: ignore[misc]

    def _raise_for_status(self, resp: httpx.Response) -> None:
        try:
            body = resp.json()
        except Exception:
            body = {}

        message = body.get("error") or body.get("detail") or resp.text
        request_id = self._config.last_request_id

        if resp.status_code == 401:
            raise AuthenticationError(message, status_code=401, body=body, request_id=request_id)
        if resp.status_code == 404:
            raise NotFoundError(message, status_code=404, body=body, request_id=request_id)
        if resp.status_code == 422:
            raise ValidationError(message, status_code=422, body=body, request_id=request_id)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "60"))
            raise RateLimitError(
                message, retry_after=retry_after, status_code=429, body=body, request_id=request_id,
            )

        raise BanklyzeError(message, status_code=resp.status_code, body=body, request_id=request_id)
