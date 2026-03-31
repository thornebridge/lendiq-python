"""Typed exceptions for the LendIQ SDK."""

from __future__ import annotations


class LendIQError(Exception):
    """Base exception for all LendIQ API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        body: dict | None = None,
        request_id: str | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.body = body or {}
        self.request_id = request_id


class AuthenticationError(LendIQError):
    """Raised on 401 — invalid or missing API key."""


class NotFoundError(LendIQError):
    """Raised on 404 — resource does not exist."""


class ValidationError(LendIQError):
    """Raised on 422 — request body failed validation."""


class RateLimitError(LendIQError):
    """Raised on 429 — rate limit exceeded."""

    def __init__(self, message: str, retry_after: int = 60, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after: int = retry_after


class InvalidSignatureError(LendIQError):
    """Raised when webhook signature verification fails."""
