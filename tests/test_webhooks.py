"""Tests for webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac

import pytest

from lendiq.exceptions import InvalidSignatureError
from lendiq.webhooks import verify_signature


def test_verify_valid_signature():
    secret = "whsec_test_secret"
    payload = b'{"event": "deal.created", "data": {}}'
    sig = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    # Should not raise
    verify_signature(payload=payload, signature=sig, secret=secret)


def test_verify_invalid_signature():
    with pytest.raises(InvalidSignatureError):
        verify_signature(
            payload=b"some payload",
            signature="sha256=invalid",
            secret="whsec_test_secret",
        )


def test_verify_missing_prefix():
    with pytest.raises(InvalidSignatureError):
        verify_signature(
            payload=b"some payload",
            signature="not_a_sha256_sig",
            secret="whsec_test_secret",
        )
