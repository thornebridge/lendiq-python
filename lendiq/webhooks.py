"""Webhook signature verification helper.

Mirrors the signing logic in the LendIQ API:
  signature = hmac.new(secret.encode(), body_bytes, sha256).hexdigest()
  header = f"sha256={signature}"
"""

from __future__ import annotations

import hashlib
import hmac

from lendiq.exceptions import InvalidSignatureError


def verify_signature(payload: bytes, signature: str, secret: str) -> None:
    """Verify a LendIQ webhook signature.

    Args:
        payload: Raw request body bytes.
        signature: Value of the X-Webhook-Signature header (e.g. "sha256=abc...").
        secret: Your webhook secret.

    Raises:
        InvalidSignatureError: If the signature does not match.
    """
    if not signature.startswith("sha256="):
        raise InvalidSignatureError("Invalid signature format — expected 'sha256=' prefix")

    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    received = signature[len("sha256="):]

    if not hmac.compare_digest(expected, received):
        raise InvalidSignatureError("Webhook signature verification failed")
