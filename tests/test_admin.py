"""Test AdminResource methods — now with typed returns."""

from __future__ import annotations

import warnings

import pytest

from lendiq.types.admin import (
    ErrorLogListResponse,
    HealthResponse,
    UsageDailyResponse,
    UsageModelsResponse,
    UsageSummaryResponse,
)
from lendiq.types.dlq import DlqActionResponse, DlqListResponse
from tests.conftest import make_response


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

SAMPLE_USAGE_SUMMARY = {
    "period_days": 30,
    "totals": {"total_calls": 150, "total_tokens": 500000, "total_cost": 2.50},
    "by_event_type": [
        {
            "event_type": "extraction",
            "count": 100,
            "input_tokens": 300000,
            "output_tokens": 50000,
            "total_tokens": 350000,
            "cost": 1.75,
            "avg_duration_ms": 2500.0,
        }
    ],
    "by_model": [
        {
            "model_name": "claude-haiku-4-5",
            "count": 100,
            "input_tokens": 300000,
            "output_tokens": 50000,
            "cost": 1.75,
            "avg_duration_ms": 2500.0,
        }
    ],
    "document_counts": {"completed": 45, "failed": 3},
    "error_counts": {"extraction": 2, "screening": 1},
}

SAMPLE_USAGE_DAILY = {
    "days": [
        {"day": "2026-02-01", "events": 10, "tokens": 25000, "cost": 0.12},
        {"day": "2026-02-02", "events": 15, "tokens": 30000, "cost": 0.18},
    ]
}

SAMPLE_USAGE_MODELS = {
    "models": [
        {
            "model_name": "claude-haiku-4-5",
            "count": 100,
            "input_tokens": 300000,
            "output_tokens": 50000,
            "cost": 1.75,
            "avg_duration_ms": 2500.0,
        }
    ]
}

SAMPLE_DLQ_LIST = {
    "data": [
        {
            "id": 1,
            "task_name": "run_pipeline",
            "args_json": {"statement_id": 42},
            "error_message": "Timeout",
            "attempts": 3,
            "status": "failed",
            "created_at": "2026-02-01T10:00:00",
        }
    ],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}

SAMPLE_DLQ_ACTION = {
    "status": "retried",
    "id": 1,
    "task_name": "run_pipeline",
}

SAMPLE_PIPELINE_SETTINGS = {
    "pipeline_llm": True,
    "pipeline_vision": False,
    "pipeline_ai_screening": True,
}


def test_health(mock_client):
    mock_client._responses["GET /v1/admin/health"] = make_response(200, SAMPLE_HEALTH)

    result = mock_client.admin.health()

    assert isinstance(result, HealthResponse)
    assert result.db_connected is True
    assert result.pipeline_success_rate_24h == 97.5
    assert result.pipelines_last_24h == 42
    assert result.queue_depth == 0


def test_errors(mock_client):
    mock_client._responses["GET /v1/admin/errors"] = make_response(
        200, SAMPLE_ERROR_LOG
    )

    result = mock_client.admin.errors()

    assert isinstance(result, ErrorLogListResponse)
    assert len(result.data) == 1
    assert result.data[0].severity == "error"
    assert result.data[0].source == "pipeline"
    assert result.meta.total == 1


def test_usage_summary(mock_client):
    mock_client._responses["GET /v1/admin/usage/summary"] = make_response(
        200, SAMPLE_USAGE_SUMMARY
    )

    result = mock_client.admin.usage_summary()

    assert isinstance(result, UsageSummaryResponse)
    assert result.period_days == 30
    assert result.totals.total_calls == 150
    assert len(result.by_event_type) == 1
    assert result.by_event_type[0].event_type == "extraction"


def test_usage_daily(mock_client):
    mock_client._responses["GET /v1/admin/usage/daily"] = make_response(
        200, SAMPLE_USAGE_DAILY
    )

    result = mock_client.admin.usage_daily()

    assert isinstance(result, UsageDailyResponse)
    assert len(result.days) == 2
    assert result.days[0].day == "2026-02-01"
    assert result.days[0].events == 10


def test_usage_models(mock_client):
    mock_client._responses["GET /v1/admin/usage/models"] = make_response(
        200, SAMPLE_USAGE_MODELS
    )

    result = mock_client.admin.usage_models()

    assert isinstance(result, UsageModelsResponse)
    assert len(result.models) == 1
    assert result.models[0].model_name == "claude-haiku-4-5"


def test_dlq_list(mock_client):
    mock_client._responses["GET /v1/admin/dlq"] = make_response(200, SAMPLE_DLQ_LIST)

    result = mock_client.admin.dlq_list()

    assert isinstance(result, DlqListResponse)
    assert len(result.data) == 1
    assert result.data[0].task_name == "run_pipeline"
    assert result.data[0].status == "failed"


def test_dlq_retry(mock_client):
    mock_client._responses["POST /v1/admin/dlq/1/retry"] = make_response(
        200, SAMPLE_DLQ_ACTION
    )

    result = mock_client.admin.dlq_retry(1)

    assert isinstance(result, DlqActionResponse)
    assert result.status == "retried"
    assert result.id == 1


def test_dlq_discard(mock_client):
    discard_response = {**SAMPLE_DLQ_ACTION, "status": "discarded"}
    mock_client._responses["POST /v1/admin/dlq/1/discard"] = make_response(
        200, discard_response
    )

    result = mock_client.admin.dlq_discard(1)

    assert isinstance(result, DlqActionResponse)
    assert result.status == "discarded"


def test_pipeline_settings(mock_client):
    mock_client._responses["GET /v1/admin/pipeline-settings"] = make_response(
        200, SAMPLE_PIPELINE_SETTINGS
    )

    result = mock_client.admin.pipeline_settings()

    assert isinstance(result, dict)
    assert result["pipeline_llm"] is True
    assert result["pipeline_vision"] is False


def test_update_pipeline_settings(mock_client):
    updated = {**SAMPLE_PIPELINE_SETTINGS, "pipeline_vision": True}
    mock_client._responses["PUT /v1/admin/pipeline-settings"] = make_response(
        200, updated
    )

    result = mock_client.admin.update_pipeline_settings(pipeline_vision=True)

    assert isinstance(result, dict)
    assert result["pipeline_vision"] is True


def test_get_constraints_deprecated(mock_client):
    mock_client._responses["GET /v1/admin/constraints"] = make_response(
        200, {"approve_min_score": 70}
    )

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = mock_client.admin.get_constraints()

    assert len(w) == 1
    assert issubclass(w[0].category, DeprecationWarning)
    assert "deprecated" in str(w[0].message).lower()
    assert result["approve_min_score"] == 70
