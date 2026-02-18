"""Typed exceptions for the Banklyze SDK."""

from __future__ import annotations


class BanklyzeError(Exception):
    """Base exception for all Banklyze API errors."""

    def __init__(self, message: str, status_code: int | None = None, body: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body or {}


class AuthenticationError(BanklyzeError):
    """Raised on 401 — invalid or missing API key."""


class NotFoundError(BanklyzeError):
    """Raised on 404 — resource does not exist."""


class ValidationError(BanklyzeError):
    """Raised on 422 — request body failed validation."""


class RateLimitError(BanklyzeError):
    """Raised on 429 — rate limit exceeded."""

    def __init__(self, message: str, retry_after: int = 60, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class InvalidSignatureError(BanklyzeError):
    """Raised when webhook signature verification fails."""
