"""Test RulesetsResource CRUD + set_default."""

from __future__ import annotations

import pytest

from banklyze.types.common import ActionResponse
from banklyze.types.ruleset import Ruleset, RulesetListResponse
from tests.conftest import make_response


SAMPLE_RULESET = {
    "id": 1,
    "name": "Default Ruleset",
    "description": "Standard underwriting rules",
    "is_default": True,
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
    "updated_by": "admin@banklyze.com",
}

SAMPLE_RULESET_LIST = {
    "data": [SAMPLE_RULESET],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}


def test_list(mock_client):
    mock_client._responses["GET /v1/rulesets"] = make_response(
        200, SAMPLE_RULESET_LIST
    )

    result = mock_client.rulesets.list()

    assert isinstance(result, RulesetListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], Ruleset)
    assert result.data[0].name == "Default Ruleset"
    assert result.data[0].is_default is True


def test_create(mock_client):
    new_ruleset = {**SAMPLE_RULESET, "id": 2, "name": "Conservative", "is_default": False}
    mock_client._responses["POST /v1/rulesets"] = make_response(201, new_ruleset)

    result = mock_client.rulesets.create(
        name="Conservative",
        is_default=False,
        approve_min_score=80.0,
    )

    assert isinstance(result, Ruleset)
    assert result.id == 2
    assert result.name == "Conservative"


def test_get(mock_client):
    mock_client._responses["GET /v1/rulesets/1"] = make_response(200, SAMPLE_RULESET)

    result = mock_client.rulesets.get(1)

    assert isinstance(result, Ruleset)
    assert result.id == 1
    assert result.approve_min_score == 70.0
    assert result.weight_revenue == 15.0


def test_update(mock_client):
    updated = {**SAMPLE_RULESET, "approve_min_score": 75.0}
    mock_client._responses["PUT /v1/rulesets/1"] = make_response(200, updated)

    result = mock_client.rulesets.update(1, approve_min_score=75.0)

    assert isinstance(result, Ruleset)
    assert result.approve_min_score == 75.0


def test_delete(mock_client):
    mock_client._responses["DELETE /v1/rulesets/1"] = make_response(
        200, {"status": "ok", "message": "Ruleset deleted"}
    )

    result = mock_client.rulesets.delete(1)

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"


def test_set_default(mock_client):
    mock_client._responses["POST /v1/rulesets/2/set-default"] = make_response(
        200, {"status": "ok", "message": "Ruleset set as default"}
    )

    result = mock_client.rulesets.set_default(2)

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"
    assert "default" in result.message.lower()
