"""AsyncLendIQClient — async variant of the LendIQ API client."""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

import httpx

from lendiq._base import ClientConfig
from lendiq.resources.admin import AsyncAdminResource
from lendiq.resources.instant import AsyncInstantResource
from lendiq.resources.lvl import AsyncLVLResource
from lendiq.resources.collaboration import (
    AsyncAssignmentsResource,
    AsyncCommentsResource,
    AsyncDocRequestsResource,
    AsyncTimelineResource,
    AsyncUserSearchResource,
)
from lendiq.resources.crm import AsyncCrmResource
from lendiq.resources.deals import AsyncDealsResource
from lendiq.resources.documents import AsyncDocumentsResource
from lendiq.resources.events import AsyncEventsResource
from lendiq.resources.exports import AsyncExportsResource
from lendiq.resources.ingest import AsyncIngestResource
from lendiq.resources.integrations import AsyncIntegrationsResource
from lendiq.resources.keys import AsyncKeysResource
from lendiq.resources.notifications import AsyncNotificationsResource
from lendiq.resources.oauth import AsyncOAuthResource
from lendiq.resources.onboarding import AsyncOnboardingResource
from lendiq.resources.push import AsyncPushResource
from lendiq.resources.reviews import AsyncReviewsResource
from lendiq.resources.rulesets import AsyncRulesetsResource
from lendiq.resources.sam_profiles import AsyncSAMProfilesResource
from lendiq.resources.share import AsyncSharesResource
from lendiq.resources.team import AsyncTeamResource
from lendiq.resources.transactions import AsyncTransactionsResource
from lendiq.resources.usage import AsyncUsageResource
from lendiq.resources.webhooks import AsyncWebhooksResource
from lendiq.exceptions import (
    AuthenticationError,
    LendIQError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


class AsyncLendIQClient:
    """Async LendIQ API client.

    Usage::

        async with AsyncLendIQClient(api_key="liq_live_...") as client:
            deals = await client.deals.list()
    """

    # Per-operation timeout defaults (seconds) — matches LendIQClient
    TIMEOUT_READ = 10.0
    TIMEOUT_WRITE = 30.0
    TIMEOUT_UPLOAD = 120.0
    TIMEOUT_REPORT = 300.0

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://iq.lend.works",
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_backoff: float = 0.5,
        retry_max_backoff: float = 30.0,
        logger: Any | None = None,
        gemini_model: str | None = None,
    ):
        self._config = ClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            retry_max_backoff=retry_max_backoff,
            gemini_model=gemini_model,
        )
        self._http = httpx.AsyncClient(
            base_url=self._config.base_url,
            headers=self._config._build_headers(),
            timeout=timeout,
        )
        self._logger = logger

        self.admin = AsyncAdminResource(self)
        self.lvl = AsyncLVLResource(self)
        self.instant = AsyncInstantResource(self)
        self.crm = AsyncCrmResource(self)
        self.deals = AsyncDealsResource(self)
        self.documents = AsyncDocumentsResource(self)
        self.events = AsyncEventsResource(self)
        self.transactions = AsyncTransactionsResource(self)
        self.exports = AsyncExportsResource(self)
        self.ingest = AsyncIngestResource(self)
        self.integrations = AsyncIntegrationsResource(self)
        self.keys = AsyncKeysResource(self)
        self.notifications = AsyncNotificationsResource(self)
        self.oauth = AsyncOAuthResource(self)
        self.onboarding = AsyncOnboardingResource(self)
        self.push = AsyncPushResource(self)
        self.reviews = AsyncReviewsResource(self)
        self.rulesets = AsyncRulesetsResource(self)
        self.sam_profiles = AsyncSAMProfilesResource(self)
        self.shares = AsyncSharesResource(self)
        self.team = AsyncTeamResource(self)
        self.usage = AsyncUsageResource(self)
        self.webhooks = AsyncWebhooksResource(self)

        # Sub-resources on deals
        self.deals.comments = AsyncCommentsResource(self)
        self.deals.assignments = AsyncAssignmentsResource(self)
        self.deals.doc_requests = AsyncDocRequestsResource(self)
        self.deals.timeline = AsyncTimelineResource(self)
        self.deals.users = AsyncUserSearchResource(self)

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
        data: dict | None = None,
        params: dict | None = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
        raw: bool = False,
        timeout: float | None = None,
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
            req_start = time.monotonic()
            try:
                resp = await self._http.request(
                    method,
                    path,
                    json=json,
                    data=data,
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    files=files,
                    headers=req_headers,
                    timeout=timeout or self._config.timeout,
                )

                # Capture the server-echoed request ID for debugging correlation
                self._config.last_request_id = resp.headers.get(
                    "X-Request-ID", req_headers["X-Request-ID"]
                )
                last_resp = resp

                if self._logger:
                    duration_ms = (time.monotonic() - req_start) * 1000
                    self._logger.debug(
                        "%s %s -> %d (%.0fms) [%s]",
                        method, path, resp.status_code, duration_ms,
                        self._config.last_request_id,
                    )

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
                last_exc = LendIQError(
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
                    raise LendIQError(
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

        raise LendIQError(message, status_code=resp.status_code, body=body, request_id=request_id)
