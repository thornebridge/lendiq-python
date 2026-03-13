"""Shared configuration for sync and async Banklyze clients."""

from __future__ import annotations

import random


class ClientConfig:
    """Holds configuration shared between sync and async clients."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = "https://api.banklyze.com",
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_backoff: float = 0.5,
        retry_max_backoff: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.retry_max_backoff = retry_max_backoff
        self.last_request_id: str | None = None

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _should_retry(self, method: str, status_code: int, attempt: int) -> bool:
        """Determine if a failed request should be retried."""
        if attempt >= self.max_retries:
            return False
        # For mutating methods, never retry on HTTP status codes — only
        # connection-level errors (handled in the except block) are retried.
        if method.upper() in ("POST", "PATCH", "PUT"):
            return False
        # Never retry deterministic client errors
        if status_code in (401, 403, 404, 409, 422):
            return False
        # Retry 429 (rate limit) and 5xx (server errors) for idempotent methods
        if status_code == 429 or status_code >= 500:
            return True
        return False

    def _backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay with jitter."""
        delay = self.retry_backoff * (2 ** attempt)
        delay = min(delay, self.retry_max_backoff)
        # Add jitter: +/-25%
        jitter = delay * 0.25 * (2 * random.random() - 1)
        return max(0, delay + jitter)
