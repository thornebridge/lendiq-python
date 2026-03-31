"""Test DocumentsResource methods."""

from __future__ import annotations

import pytest

from lendiq.types.document import (
    BatchDocumentStatusResponse,
    DocumentDetail,
    DocumentListResponse,
    DocumentStatusResponse,
    DocumentSummary,
)
from tests.conftest import SAMPLE_DOCUMENT, make_response


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

SAMPLE_DOCUMENT_STATUS = {
    "id": 15,
    "status": "completed",
    "document_type": "bank_statement",
    "error_message": None,
    "processing_started_at": "2026-02-01T09:15:30",
    "processing_completed_at": "2026-02-01T09:16:45",
}

SAMPLE_DOCUMENT_LIST = {
    "data": [SAMPLE_DOCUMENT],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}

SAMPLE_BATCH_STATUS = {
    "documents": {
        "15": {
            "id": 15,
            "filename": "chase_jan_2026.pdf",
            "status": "completed",
            "bank_name": "Chase",
        },
        "16": {
            "id": 16,
            "filename": "boa_feb_2026.pdf",
            "status": "processing",
            "bank_name": "Bank of America",
        },
    }
}


def test_list_documents(mock_client):
    mock_client._responses["GET /v1/deals/1/documents"] = make_response(
        200, SAMPLE_DOCUMENT_LIST
    )

    result = mock_client.documents.list(deal_id=1)

    assert isinstance(result, DocumentListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], DocumentSummary)
    assert result.data[0].filename == "chase_jan_2026.pdf"
    assert result.meta.total == 1


def test_get_document(mock_client):
    mock_client._responses["GET /v1/documents/15"] = make_response(
        200, SAMPLE_DOCUMENT_DETAIL
    )

    result = mock_client.documents.get(15)

    assert isinstance(result, DocumentDetail)
    assert result.id == 15
    assert result.bank_name == "Chase"
    assert result.account_holder_name == "Acme Trucking LLC"
    assert result.prescreen is not None
    assert result.prescreen.viable is True
    assert result.integrity is not None
    assert result.integrity.tampering_risk_level == "clean"


def test_document_status(mock_client):
    mock_client._responses["GET /v1/documents/15/status"] = make_response(
        200, SAMPLE_DOCUMENT_STATUS
    )

    result = mock_client.documents.status(15)

    assert isinstance(result, DocumentStatusResponse)
    assert result.id == 15
    assert result.status == "completed"
    assert result.document_type == "bank_statement"


def test_reprocess(mock_client):
    mock_client._responses["POST /v1/documents/15/reprocess"] = make_response(
        200, SAMPLE_DOCUMENT_STATUS
    )

    result = mock_client.documents.reprocess(15)

    assert isinstance(result, DocumentStatusResponse)
    assert result.id == 15
    assert result.status == "completed"


def test_cancel(mock_client):
    cancel_response = {**SAMPLE_DOCUMENT_STATUS, "status": "cancelled"}
    mock_client._responses["POST /v1/documents/15/cancel"] = make_response(
        200, cancel_response
    )

    result = mock_client.documents.cancel(15)

    assert isinstance(result, DocumentStatusResponse)
    assert result.status == "cancelled"


def test_reclassify(mock_client):
    reclassified = {**SAMPLE_DOCUMENT_STATUS, "document_type": "tax_return"}
    mock_client._responses["POST /v1/documents/15/reclassify"] = make_response(
        200, reclassified
    )

    result = mock_client.documents.reclassify(15, document_type="tax_return")

    assert isinstance(result, DocumentStatusResponse)
    assert result.document_type == "tax_return"


def test_batch_status(mock_client):
    mock_client._responses["POST /v1/documents/batch-status"] = make_response(
        200, SAMPLE_BATCH_STATUS
    )

    result = mock_client.documents.batch_status(document_ids=[15, 16])

    assert isinstance(result, BatchDocumentStatusResponse)
    assert "15" in result.documents
    assert result.documents["15"].status == "completed"
    assert result.documents["16"].status == "processing"
