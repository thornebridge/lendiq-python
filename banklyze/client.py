"""BanklyzeClient — Stripe-style synchronous API client."""

from __future__ import annotations

import time
import uuid
from typing import Any

import httpx

from banklyze._base import ClientConfig
from banklyze.exceptions import (
    AuthenticationError,
    BanklyzeError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from banklyze.resources.admin import AdminResource
from banklyze.resources.bvl import BVLResource
from banklyze.resources.collaboration import (
    AssignmentsResource,
    CommentsResource,
    DocRequestsResource,
    TimelineResource,
    UserSearchResource,
)
from banklyze.resources.crm import CrmResource
from banklyze.resources.deals import DealsResource
from banklyze.resources.documents import DocumentsResource
from banklyze.resources.events import EventsResource
from banklyze.resources.exports import ExportsResource
from banklyze.resources.ingest import IngestResource
from banklyze.resources.integrations import IntegrationsResource
from banklyze.resources.keys import KeysResource
from banklyze.resources.notifications import NotificationsResource
from banklyze.resources.oauth import OAuthResource
from banklyze.resources.onboarding import OnboardingResource
from banklyze.resources.push import PushResource
from banklyze.resources.reviews import ReviewsResource
from banklyze.resources.rulesets import RulesetsResource
from banklyze.resources.sam_profiles import SAMProfilesResource
from banklyze.resources.share import SharesResource
from banklyze.resources.team import TeamResource
from banklyze.resources.transactions import TransactionsResource
from banklyze.resources.usage import UsageResource
from banklyze.resources.webhooks import WebhooksResource


class BanklyzeClient:
    """Banklyze API client.

    Usage::

        client = BanklyzeClient(api_key="bk_live_...", base_url="https://api.banklyze.com")
        deals = client.deals.list()

    Or as a context manager::

        with BanklyzeClient(api_key="bk_live_...") as client:
            deals = client.deals.list()
    """

    # Per-operation timeout defaults (seconds)
    TIMEOUT_READ = 10.0
    TIMEOUT_WRITE = 30.0
    TIMEOUT_UPLOAD = 120.0
    TIMEOUT_REPORT = 300.0

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.banklyze.com",
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_backoff: float = 0.5,
        retry_max_backoff: float = 30.0,
        logger: Any | None = None,
    ):
        self._config = ClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            retry_max_backoff=retry_max_backoff,
        )
        self._http = httpx.Client(
            base_url=self._config.base_url,
            headers=self._config._build_headers(),
            timeout=timeout,
        )
        self._logger = logger

        self.admin = AdminResource(self)
        self.bvl = BVLResource(self)
        self.crm = CrmResource(self)
        self.deals = DealsResource(self)
        self.documents = DocumentsResource(self)
        self.events = EventsResource(self)
        self.transactions = TransactionsResource(self)
        self.exports = ExportsResource(self)
        self.ingest = IngestResource(self)
        self.integrations = IntegrationsResource(self)
        self.keys = KeysResource(self)
        self.notifications = NotificationsResource(self)
        self.oauth = OAuthResource(self)
        self.onboarding = OnboardingResource(self)
        self.push = PushResource(self)
        self.reviews = ReviewsResource(self)
        self.rulesets = RulesetsResource(self)
        self.sam_profiles = SAMProfilesResource(self)
        self.shares = SharesResource(self)
        self.team = TeamResource(self)
        self.usage = UsageResource(self)
        self.webhooks = WebhooksResource(self)

        # Sub-resources on deals
        self.deals.comments = CommentsResource(self)
        self.deals.assignments = AssignmentsResource(self)
        self.deals.doc_requests = DocRequestsResource(self)
        self.deals.timeline = TimelineResource(self)
        self.deals.users = UserSearchResource(self)

    @property
    def last_request_id(self) -> str | None:
        return self._config.last_request_id

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self) -> None:
        self._http.close()

    # ── Internal request helpers ─────────────────────────────────────────────

    def _request(
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
        """Make an API request and return parsed JSON (or raw bytes if raw=True).

        Automatically retries on transient failures with exponential backoff.
        For mutating methods (POST/PATCH/PUT), only connection-level errors are
        retried (the request never reached the server). For idempotent methods
        (GET/DELETE/HEAD/OPTIONS), retryable HTTP status codes (429, 5xx) are
        also retried.
        """
        req_headers = dict(headers or {})
        req_headers["X-Request-ID"] = str(uuid.uuid4())

        last_exc: Exception | None = None
        resp: httpx.Response | None = None

        for attempt in range(1 + self._config.max_retries):
            req_start = time.monotonic()
            try:
                resp = self._http.request(
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

                time.sleep(delay)
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
                time.sleep(self._config._backoff_delay(attempt))

        # Exhausted retries — raise the last error
        if resp is not None:
            self._raise_for_status(resp)

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
