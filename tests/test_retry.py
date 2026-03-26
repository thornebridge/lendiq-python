"""Test retry logic — exponential backoff, 429 handling, POST safety."""

from __future__ import annotations

import json
import time

import httpx
import pytest

from banklyze import BanklyzeClient
from banklyze.exceptions import AuthenticationError, BanklyzeError, RateLimitError, ValidationError
from tests.conftest import SAMPLE_DEAL_LIST, make_response


def _make_client(handler, *, max_retries: int = 2, retry_backoff: float = 0.1):
    """Create a BanklyzeClient with a custom mock transport handler."""
    transport = httpx.MockTransport(handler)
    client = BanklyzeClient(
        api_key="bk_test_xxx",
        base_url="https://test.banklyze.com",
        max_retries=max_retries,
        retry_backoff=retry_backoff,
    )
    client._http = httpx.Client(
        transport=transport,
        base_url="https://test.banklyze.com",
        headers={"X-API-Key": "bk_test_xxx"},
    )
    return client


def test_retry_429_on_get(monkeypatch):
    """GET returns 429 twice then 200 on the third attempt; 3 total calls."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        if len(call_log) <= 2:
            return make_response(
                429,
                {"error": "Rate limited"},
                headers={"Retry-After": "0"},
            )
        return make_response(200, SAMPLE_DEAL_LIST)

    client = _make_client(handler)
    result = client.deals.list()

    assert len(call_log) == 3
    assert result.data[0].business_name == "Acme Trucking LLC"
    client.close()


def test_retry_500_on_get(monkeypatch):
    """GET returns 500 then 200; 2 total calls."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        if len(call_log) <= 1:
            return make_response(500, {"error": "Server error"})
        return make_response(200, SAMPLE_DEAL_LIST)

    client = _make_client(handler)
    result = client.deals.list()

    assert len(call_log) == 2
    assert result.meta.total == 1
    client.close()


def test_no_retry_post_on_500(monkeypatch):
    """POST returns 500; exactly 1 call, raises BanklyzeError."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        return make_response(500, {"error": "Server error"})

    client = _make_client(handler)
    with pytest.raises(BanklyzeError):
        client.deals.create(business_name="Test")

    assert len(call_log) == 1
    client.close()


def test_no_retry_on_401(monkeypatch):
    """401 is never retried regardless of method — 1 call, raises AuthenticationError."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        return make_response(401, {"error": "Invalid key"})

    client = _make_client(handler)
    with pytest.raises(AuthenticationError):
        client.deals.list()

    assert len(call_log) == 1
    client.close()


def test_no_retry_on_422(monkeypatch):
    """422 is never retried — 1 call, raises ValidationError."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        return make_response(422, {"detail": "bad field"})

    client = _make_client(handler)
    with pytest.raises(ValidationError):
        client.deals.create(business_name="Test")

    assert len(call_log) == 1
    client.close()


def test_max_retries_exhausted(monkeypatch):
    """429 every time; raises after max_retries+1 calls."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        return make_response(
            429,
            {"error": "Rate limited"},
            headers={"Retry-After": "0"},
        )

    client = _make_client(handler, max_retries=2)
    with pytest.raises(RateLimitError):
        client.deals.list()

    # 1 initial + 2 retries = 3 total calls
    assert len(call_log) == 3
    client.close()


def test_retry_after_header_honored(monkeypatch):
    """429 with Retry-After: verify time.sleep is called with the header value."""
    sleep_delays = []
    monkeypatch.setattr(time, "sleep", lambda s: sleep_delays.append(s))
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        if len(call_log) <= 1:
            return make_response(
                429,
                {"error": "Rate limited"},
                headers={"Retry-After": "5"},
            )
        return make_response(200, SAMPLE_DEAL_LIST)

    client = _make_client(handler, max_retries=2)
    client.deals.list()

    assert len(call_log) == 2
    # The sleep delay should be the Retry-After value (5.0)
    assert len(sleep_delays) == 1
    assert sleep_delays[0] == 5.0
    client.close()


def test_connection_error_retried_get(monkeypatch):
    """Connection errors are retried for GET requests."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        if len(call_log) <= 1:
            raise httpx.ConnectError("Connection refused")
        return make_response(200, SAMPLE_DEAL_LIST)

    client = _make_client(handler, max_retries=2)
    result = client.deals.list()

    assert len(call_log) == 2
    assert result.data[0].business_name == "Acme Trucking LLC"
    client.close()


def test_connection_error_retried_post(monkeypatch):
    """Connection errors are retried even for POST (never reached server)."""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_log = []

    from tests.conftest import SAMPLE_DEAL

    def handler(request: httpx.Request) -> httpx.Response:
        call_log.append(request.method)
        if len(call_log) <= 1:
            raise httpx.ConnectError("Connection refused")
        return make_response(201, SAMPLE_DEAL)

    client = _make_client(handler, max_retries=2)
    result = client.deals.create(business_name="Test")

    assert len(call_log) == 2
    assert result.business_name == "Acme Trucking LLC"
    client.close()
