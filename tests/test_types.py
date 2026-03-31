"""Tests for response type parsing and forward compatibility."""

from __future__ import annotations

from lendiq.types import (
    DealDetail,
    DealListResponse,
    DealSummary,
    PaginationMeta,
    Transaction,
    WebhookConfig,
)


def test_deal_summary_from_dict():
    data = {
        "id": 1,
        "business_name": "Acme",
        "status": "ready",
        "health_score": 72.5,
        "unknown_future_field": True,
    }
    deal = DealSummary.model_validate(data)
    assert deal.id == 1
    assert deal.business_name == "Acme"
    assert deal.health_score == 72.5
    # Forward compatibility
    assert deal.unknown_future_field is True  # type: ignore[attr-defined]


def test_deal_list_response_from_dict():
    data = {
        "data": [
            {"id": 1, "business_name": "Acme", "status": "ready"},
            {"id": 2, "business_name": "Beta Co", "status": "new"},
        ],
        "meta": {"page": 1, "per_page": 25, "total": 2, "total_pages": 1},
    }
    response = DealListResponse.model_validate(data)
    assert len(response.data) == 2
    assert response.data[0].business_name == "Acme"
    assert response.meta.total == 2


def test_deal_detail_with_nested_types():
    data = {
        "report_date": "2026-02-14",
        "business": {"business_name": "Acme", "industry": "Transport"},
        "coverage": {"total_days_covered": 90},
        "financials": {"avg_monthly_deposits": 85000.0},
        "nsf_overdraft": {"nsf_fee_count": 2},
        "screening": {"suspicious_count": 0},
        "health": {"health_score": 72.5, "health_grade": "B"},
        "owner": {"name": "John Smith", "credit_score": 720},
        "mca": {"positions_detected": 2, "total_daily_obligation": 450.0},
        "recommendation": {"decision": "approve", "paper_grade": "B"},
    }
    detail = DealDetail.model_validate(data)
    assert detail.business.industry == "Transport"
    assert detail.owner.name == "John Smith"
    assert detail.owner.credit_score == 720
    assert detail.mca.positions_detected == 2
    assert detail.health.health_grade == "B"
    assert detail.recommendation.decision == "approve"


def test_transaction_parsing():
    data = {
        "id": 101,
        "date": "2026-01-15",
        "description": "ACH DEPOSIT",
        "amount": "4250.00",
        "balance": "18340.50",
        "transaction_type": "deposit",
        "is_nsf_fee": False,
        "is_suspicious": False,
    }
    txn = Transaction.model_validate(data)
    assert txn.id == 101
    assert float(txn.amount) == 4250.00
    assert txn.transaction_type == "deposit"


def test_webhook_config_defaults():
    data = {"url": "https://example.com/hook", "events": ["deal.created"]}
    config = WebhookConfig.model_validate(data)
    assert config.enabled is True
    assert config.has_secret is False


def test_pagination_meta():
    data = {"page": 2, "per_page": 50, "total": 150, "total_pages": 3}
    meta = PaginationMeta.model_validate(data)
    assert meta.page == 2
    assert meta.total_pages == 3
