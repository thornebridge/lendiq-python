"""Test error handling — correct exception types for each HTTP status code."""

from __future__ import annotations

import pytest

from lendiq.exceptions import (
    AuthenticationError,
    LendIQError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from tests.conftest import SAMPLE_DEAL_LIST, make_response


def test_401_raises_authentication_error(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(
        401, {"error": "Invalid API key"}
    )

    with pytest.raises(AuthenticationError) as exc_info:
        mock_client.deals.list()

    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)


def test_404_raises_not_found_error(mock_client):
    mock_client._responses["GET /v1/deals/999"] = make_response(
        404, {"error": "Deal not found"}
    )

    with pytest.raises(NotFoundError) as exc_info:
        mock_client.deals.get(999)

    assert exc_info.value.status_code == 404
    assert "Deal not found" in str(exc_info.value)


def test_422_raises_validation_error(mock_client):
    mock_client._responses["POST /v1/deals"] = make_response(
        422, {"detail": "business_name is required"}
    )

    with pytest.raises(ValidationError) as exc_info:
        mock_client.deals.create(business_name="")

    assert exc_info.value.status_code == 422
    assert "business_name is required" in str(exc_info.value)


def test_429_raises_rate_limit_error(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(
        429,
        {"error": "Rate limit exceeded"},
        headers={"Retry-After": "30"},
    )

    with pytest.raises(RateLimitError) as exc_info:
        mock_client.deals.list()

    assert exc_info.value.status_code == 429
    assert exc_info.value.retry_after == 30


def test_500_raises_lendiq_error(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(
        500, {"error": "Internal server error"}
    )

    with pytest.raises(LendIQError) as exc_info:
        mock_client.deals.list()

    assert exc_info.value.status_code == 500
    assert "Internal server error" in str(exc_info.value)


def test_error_body_preserved(mock_client):
    body = {"error": "Invalid API key", "code": "AUTH_FAILED", "extra": "data"}
    mock_client._responses["GET /v1/deals"] = make_response(401, body)

    with pytest.raises(AuthenticationError) as exc_info:
        mock_client.deals.list()

    assert exc_info.value.body == body
    assert exc_info.value.body["code"] == "AUTH_FAILED"


def test_request_id_on_error(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(
        404,
        {"error": "Deal not found"},
        headers={"X-Request-ID": "req-abc-123"},
    )

    with pytest.raises(NotFoundError) as exc_info:
        mock_client.deals.list()

    assert exc_info.value.request_id == "req-abc-123"


def test_error_message_from_error_key(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(
        500, {"error": "Something broke"}
    )

    with pytest.raises(LendIQError) as exc_info:
        mock_client.deals.list()

    assert "Something broke" in str(exc_info.value)


def test_error_message_from_detail_key(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(
        422, {"detail": "Field X is invalid"}
    )

    with pytest.raises(ValidationError) as exc_info:
        mock_client.deals.list()

    assert "Field X is invalid" in str(exc_info.value)
