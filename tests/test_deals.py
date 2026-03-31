"""Tests for the deals resource with typed responses."""

from __future__ import annotations

import pytest

from lendiq.types import DealListResponse, DealSummary, DealStats
from lendiq.types.common import ActionResponse
from lendiq.types.deal import (
    DailyStatsResponse,
    DealAnalyticsResponse,
    DealDetail,
    DealNote,
    DealNotesListResponse,
)
from lendiq.types.ruleset import ComparativeEvaluationResponse
from lendiq.types.underwriting import Recommendation
from tests.conftest import SAMPLE_DEAL, SAMPLE_DEAL_LIST, make_response


def test_list_deals(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(200, SAMPLE_DEAL_LIST)

    result = mock_client.deals.list()

    assert isinstance(result, DealListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], DealSummary)
    assert result.data[0].business_name == "Acme Trucking LLC"
    assert result.data[0].health_score == 72.5
    assert result.meta.page == 1
    assert result.meta.total == 1


def test_create_deal(mock_client):
    mock_client._responses["POST /v1/deals"] = make_response(201, SAMPLE_DEAL)

    result = mock_client.deals.create(
        business_name="Acme Trucking LLC",
        funding_amount_requested=75000,
    )

    assert isinstance(result, DealSummary)
    assert result.id == 1
    assert result.business_name == "Acme Trucking LLC"


def test_get_deal_stats(mock_client):
    stats_data = {
        "total": 42,
        "by_status": {"ready": 10, "approved": 20},
        "total_volume": 1250000.00,
        "avg_health": 68.5,
    }
    mock_client._responses["GET /v1/deals/stats"] = make_response(200, stats_data)

    result = mock_client.deals.stats()

    assert isinstance(result, DealStats)
    assert result.total == 42
    assert result.by_status["ready"] == 10


def test_deal_forward_compatibility(mock_client):
    """Unknown fields from API are preserved (extra='allow')."""
    deal_with_new_field = {**SAMPLE_DEAL, "new_field": "new_value"}
    mock_client._responses["POST /v1/deals"] = make_response(201, deal_with_new_field)

    result = mock_client.deals.create(business_name="Test", funding_amount_requested=50000)

    assert result.new_field == "new_value"  # type: ignore[attr-defined]


# ── Sample data for new tests ───────────────────────────────────────────────

SAMPLE_DEAL_DETAIL = {
    "report_date": "2026-02-14",
    "business": {"business_name": "Acme Trucking LLC", "industry": "Transport"},
    "coverage": {"total_days_covered": 90, "document_count": 3},
    "financials": {"avg_monthly_deposits": 85000.0, "avg_daily_balance": 12340.50},
    "nsf_overdraft": {"nsf_fee_count": 2, "overdraft_fee_count": 0},
    "screening": {"suspicious_count": 0},
    "health": {"health_score": 72.5, "health_grade": "B"},
    "owner": {"name": "John Smith", "credit_score": 720},
    "mca": {"positions_detected": 2, "total_daily_obligation": 450.0},
    "recommendation": {"decision": "approve", "paper_grade": "B"},
}

SAMPLE_NOTE = {
    "id": 50,
    "deal_id": 1,
    "author": "API",
    "content": "Reviewed all statements.",
    "note_type": "internal",
    "created_at": "2026-02-15T10:00:00",
}

SAMPLE_NOTES_LIST = {
    "data": [SAMPLE_NOTE],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}

SAMPLE_RECOMMENDATION = {
    "id": 1,
    "deal_id": 1,
    "decision": "approve",
    "weighted_score": 75.3,
    "risk_tier": "low",
    "paper_grade": "B",
    "advance_amount": 60000.0,
    "factor_rate": 1.35,
    "holdback_pct": 12.0,
    "risk_factors": ["2 existing MCA positions"],
    "strengths": ["Strong deposit consistency", "Low NSF count"],
    "hard_decline_reasons": [],
    "confidence": 0.85,
    "confidence_label": "high",
    "created_at": "2026-02-14T12:00:00",
}

SAMPLE_DAILY_STATS = {
    "period_days": 30,
    "data": [
        {
            "date": "2026-02-01",
            "total": 5,
            "approved": 3,
            "declined": 1,
            "funded": 1,
            "avg_score": 72.0,
        },
        {
            "date": "2026-02-02",
            "total": 8,
            "approved": 5,
            "declined": 2,
            "funded": 1,
            "avg_score": 68.5,
        },
    ],
}

SAMPLE_COMPARATIVE_EVAL = {
    "deal_id": 1,
    "evaluations": [
        {
            "ruleset_name": "Default Ruleset",
            "decision": "approve",
            "weighted_score": 75.3,
            "risk_tier": "low",
            "paper_grade": "B",
            "risk_factors": [],
            "strengths": ["Strong deposits"],
            "hard_decline_reasons": [],
        },
        {
            "ruleset_name": "Conservative Ruleset",
            "decision": "conditional",
            "weighted_score": 62.1,
            "risk_tier": "medium",
            "paper_grade": "C",
            "risk_factors": ["Below revenue threshold"],
            "strengths": [],
            "hard_decline_reasons": [],
        },
    ],
    "best_fit": {
        "ruleset_name": "Default Ruleset",
        "decision": "approve",
        "weighted_score": 75.3,
        "risk_tier": "low",
        "risk_factors": [],
        "strengths": ["Strong deposits"],
        "hard_decline_reasons": [],
    },
}


# ── New tests ────────────────────────────────────────────────────────────────


def test_get_deal(mock_client):
    mock_client._responses["GET /v1/deals/1"] = make_response(200, SAMPLE_DEAL_DETAIL)

    result = mock_client.deals.get(1)

    assert isinstance(result, DealDetail)
    assert result.report_date == "2026-02-14"
    assert result.business.business_name == "Acme Trucking LLC"
    assert result.health.health_score == 72.5
    assert result.health.health_grade == "B"
    assert result.owner.name == "John Smith"
    assert result.mca.positions_detected == 2


def test_update_deal(mock_client):
    updated = {**SAMPLE_DEAL, "business_name": "Acme Trucking Inc"}
    mock_client._responses["PATCH /v1/deals/1"] = make_response(200, updated)

    result = mock_client.deals.update(1, business_name="Acme Trucking Inc")

    assert isinstance(result, DealSummary)
    assert result.business_name == "Acme Trucking Inc"


def test_delete_deal(mock_client):
    mock_client._responses["DELETE /v1/deals/1"] = make_response(
        200, {"status": "ok", "message": "Deal deleted"}
    )

    result = mock_client.deals.delete(1)

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"


def test_decision(mock_client):
    mock_client._responses["POST /v1/deals/1/decision"] = make_response(
        200, {"status": "ok", "message": "Deal approved"}
    )

    result = mock_client.deals.decision(1, decision="approved")

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"


def test_evaluate(mock_client):
    mock_client._responses["POST /v1/deals/1/evaluate"] = make_response(
        200, SAMPLE_COMPARATIVE_EVAL
    )

    result = mock_client.deals.evaluate(1, ruleset_ids=[1, 2])

    assert isinstance(result, ComparativeEvaluationResponse)
    assert result.deal_id == 1
    assert len(result.evaluations) == 2
    assert result.evaluations[0].decision == "approve"
    assert result.evaluations[1].decision == "conditional"
    assert result.best_fit is not None
    assert result.best_fit.ruleset_name == "Default Ruleset"


def test_notes_list(mock_client):
    mock_client._responses["GET /v1/deals/1/notes"] = make_response(
        200, SAMPLE_NOTES_LIST
    )

    result = mock_client.deals.notes(1)

    assert isinstance(result, DealNotesListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], DealNote)
    assert result.data[0].content == "Reviewed all statements."
    assert result.meta.total == 1


def test_add_note(mock_client):
    mock_client._responses["POST /v1/deals/1/notes"] = make_response(
        201, SAMPLE_NOTE
    )

    result = mock_client.deals.add_note(1, content="Reviewed all statements.")

    assert isinstance(result, DealNote)
    assert result.id == 50
    assert result.content == "Reviewed all statements."
    assert result.author == "API"


def test_recommendation(mock_client):
    mock_client._responses["GET /v1/deals/1/recommendation"] = make_response(
        200, SAMPLE_RECOMMENDATION
    )

    result = mock_client.deals.recommendation(1)

    assert isinstance(result, Recommendation)
    assert result.decision == "approve"
    assert result.weighted_score == 75.3
    assert result.paper_grade == "B"
    assert result.advance_amount == 60000.0
    assert len(result.strengths) == 2
    assert result.confidence == 0.85


def test_daily_stats(mock_client):
    mock_client._responses["GET /v1/deals/stats/daily"] = make_response(
        200, SAMPLE_DAILY_STATS
    )

    result = mock_client.deals.daily_stats(days=30)

    assert isinstance(result, DailyStatsResponse)
    assert result.period_days == 30
    assert len(result.data) == 2
    assert result.data[0].date == "2026-02-01"
    assert result.data[0].total == 5
    assert result.data[0].approved == 3


def test_analytics(mock_client):
    mock_client._responses["GET /v1/deals/analytics"] = make_response(
        200, {"approval_rate": 0.75, "avg_funding": 65000.0}
    )

    result = mock_client.deals.analytics()

    assert isinstance(result, DealAnalyticsResponse)
    # Forward compatibility: extra fields are allowed
    assert result.approval_rate == 0.75  # type: ignore[attr-defined]


def test_batch_create(mock_client):
    mock_client._responses["POST /v1/deals/batch"] = make_response(
        201,
        {
            "created": 2,
            "deals": [
                {"id": 10, "business_name": "Alpha Inc"},
                {"id": 11, "business_name": "Beta LLC"},
            ],
        },
    )

    result = mock_client.deals.batch_create(
        deals=[
            {"business_name": "Alpha Inc"},
            {"business_name": "Beta LLC"},
        ]
    )

    assert isinstance(result, dict)
    assert result["created"] == 2
    assert len(result["deals"]) == 2
