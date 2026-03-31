"""Shared fixtures for SDK tests."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from lendiq import LendIQClient


def make_response(
    status_code: int = 200,
    json_data: dict[str, Any] | None = None,
    content: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Build a mock httpx.Response."""
    resp_headers = {"X-Request-ID": "test-req-id", **(headers or {})}
    if json_data is not None:
        return httpx.Response(
            status_code,
            content=json.dumps(json_data).encode(),
            headers={**resp_headers, "content-type": "application/json"},
        )
    return httpx.Response(
        status_code,
        content=content or b"",
        headers=resp_headers,
    )


SAMPLE_DEAL = {
    "id": 1,
    "business_name": "Acme Trucking LLC",
    "status": "ready",
    "document_count": 3,
    "health_score": 72.5,
    "health_grade": "B",
    "avg_monthly_deposits": 85432.10,
    "avg_daily_balance": 12340.50,
    "funding_amount_requested": 75000.00,
    "screening_flags": 2,
    "created_at": "2026-01-15T10:30:00",
    "updated_at": "2026-01-16T14:22:00",
}

SAMPLE_DEAL_LIST = {
    "data": [SAMPLE_DEAL],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}

SAMPLE_DOCUMENT = {
    "id": 15,
    "filename": "chase_jan_2026.pdf",
    "document_type": "bank_statement",
    "bank_name": "Chase",
    "status": "completed",
    "health_grade": "B",
    "created_at": "2026-02-01T09:15:30",
}

SAMPLE_DOCUMENT_DETAIL = {
    "id": 15,
    "filename": "chase_jan_2026.pdf",
    "document_type": "bank_statement",
    "bank_name": "Chase",
    "account_holder_name": "Acme Trucking LLC",
    "statement_start_date": "2026-01-01",
    "statement_end_date": "2026-01-31",
    "status": "completed",
    "prescreen": {
        "bank_name": "Chase",
        "opening_balance": 15000.0,
        "closing_balance": 18000.0,
        "viable": True,
        "confidence": 0.95,
        "text_quality": 0.9,
    },
    "integrity": {
        "tampering_risk_level": "clean",
        "tampering_flags": [],
    },
    "analysis": {
        "average_daily_balance": 16500.0,
        "total_deposits": 95000.0,
        "deposit_count": 24,
    },
    "created_at": "2026-02-01T09:15:30",
    "updated_at": "2026-02-01T10:30:00",
}

SAMPLE_TRANSACTION = {
    "id": 101,
    "document_id": 15,
    "date": "2026-01-15",
    "description": "ACH DEPOSIT - STRIPE",
    "amount": 4500.00,
    "balance": 19500.00,
    "type": "deposit",
    "flagged": False,
    "category": "payment_processor",
}

SAMPLE_RULESET = {
    "id": 1,
    "name": "Default Ruleset",
    "is_default": True,
    "description": "Standard underwriting rules",
    "min_monthly_deposits": 10000.0,
    "min_days_covered": 60,
    "min_health_score": 40.0,
    "max_suspicious_count": 5,
    "max_nsf_per_month": 3.0,
    "max_debt_service_ratio": 0.75,
    "min_adb_pct_of_revenue": 0.10,
    "min_deposit_frequency": 15,
    "revenue_decline_red_flag_pct": 0.30,
    "approve_min_score": 70.0,
    "conditional_min_score": 50.0,
    "grade_a_min_score": 80.0,
    "grade_b_min_score": 65.0,
    "grade_c_min_score": 50.0,
    "min_cfcr": 1.25,
    "weight_revenue": 15.0,
    "weight_balance_health": 10.0,
    "weight_nsf_overdraft": 10.0,
    "weight_deposit_frequency": 5.0,
    "weight_revenue_trend": 10.0,
    "weight_debt_service": 10.0,
    "weight_transaction_screening": 10.0,
    "weight_health_score": 10.0,
    "weight_cross_doc": 5.0,
    "weight_position_stacking": 5.0,
    "weight_cash_flow_volatility": 5.0,
    "weight_revenue_quality": 3.0,
    "weight_daily_velocity": 2.0,
    "updated_at": "2026-01-01T00:00:00",
    "updated_by": "admin@lendiq.com",
}

SAMPLE_HEALTH = {
    "db_connected": True,
    "pipeline_success_rate_24h": 97.5,
    "pipelines_last_24h": 42,
    "queue_depth": 0,
}

SAMPLE_ERROR_LOG = {
    "data": [
        {
            "id": 1,
            "severity": "error",
            "source": "pipeline",
            "message": "extraction failed",
            "created_at": "2026-02-01T09:00:00",
        }
    ],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}


@pytest.fixture
def mock_client(monkeypatch):
    """LendIQClient with a mock transport that returns canned responses."""
    responses: dict[str, httpx.Response] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        key = f"{request.method} {request.url.path}"
        if key in responses:
            return responses[key]
        # Default: 404
        return make_response(404, {"error": "Not found", "code": "RESOURCE_NOT_FOUND"})

    transport = httpx.MockTransport(handler)
    client = LendIQClient(api_key="liq_test_xxx", base_url="https://test.lendiq.com")
    # Replace the real transport with our mock
    client._http = httpx.Client(
        transport=transport,
        base_url="https://test.lendiq.com",
        headers={"X-API-Key": "liq_test_xxx"},
    )
    client._responses = responses  # type: ignore[attr-defined]
    return client
