"""Test collaboration sub-resources — comments, assignments, doc_requests, timeline, user_search."""

from __future__ import annotations

import pytest

from banklyze.types.collaboration import (
    AssignedDealsResponse,
    Assignment,
    AssignmentListResponse,
    Comment,
    CommentListResponse,
    DocRequest,
    DocRequestListResponse,
    TimelineResponse,
    UserSearchResponse,
)
from banklyze.types.common import ActionResponse
from tests.conftest import make_response


# ── Sample data ─────────────────────────────────────────────────────────────

SAMPLE_COMMENT = {
    "id": 10,
    "deal_id": 1,
    "author_id": 5,
    "parent_id": None,
    "content": "Looks good to approve.",
    "mentions": [],
    "created_at": "2026-02-10T14:30:00",
    "updated_at": "2026-02-10T14:30:00",
    "author_email": "analyst@banklyze.com",
    "author_display_name": "Jane Analyst",
}

SAMPLE_COMMENT_LIST = {"data": [SAMPLE_COMMENT]}

SAMPLE_ASSIGNMENT = {
    "id": 20,
    "deal_id": 1,
    "user_id": 5,
    "role": "assignee",
    "assigned_by_id": 3,
    "created_at": "2026-02-10T10:00:00",
    "user_email": "analyst@banklyze.com",
    "user_display_name": "Jane Analyst",
}

SAMPLE_ASSIGNMENT_LIST = {"data": [SAMPLE_ASSIGNMENT]}

SAMPLE_DOC_REQUEST = {
    "id": 30,
    "deal_id": 1,
    "document_type": "bank_statement",
    "description": "Need January 2026 statement",
    "recipient_email": "owner@acme.com",
    "status": "pending",
    "due_date": "2026-03-01",
    "fulfilled_at": None,
    "document_id": None,
    "created_at": "2026-02-15T09:00:00",
    "updated_at": "2026-02-15T09:00:00",
}

SAMPLE_DOC_REQUEST_LIST = {"data": [SAMPLE_DOC_REQUEST]}

SAMPLE_TIMELINE = {
    "data": [
        {
            "id": 100,
            "event_type": "deal.created",
            "summary": "Deal created: Acme Trucking LLC",
            "actor_name": "John Admin",
            "actor_id": 3,
            "deal_id": 1,
            "metadata": {},
            "created_at": "2026-02-01T08:00:00",
        }
    ],
    "meta": {"page": 1, "per_page": 50, "total": 1, "total_pages": 1},
}

SAMPLE_USER_SEARCH = {
    "data": [
        {
            "id": 5,
            "email": "analyst@banklyze.com",
            "display_name": "Jane Analyst",
            "role": "analyst",
        }
    ]
}

SAMPLE_ASSIGNED_DEALS = {
    "data": [
        {
            "id": 1,
            "business_name": "Acme Trucking LLC",
            "status": "ready",
            "health_grade": "B",
            "updated_at": "2026-02-15T10:00:00",
        }
    ],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}


# ── Comments tests ──────────────────────────────────────────────────────────


def test_comments_list(mock_client):
    mock_client._responses["GET /v1/deals/1/comments"] = make_response(
        200, SAMPLE_COMMENT_LIST
    )

    result = mock_client.deals.comments.list(1)

    assert isinstance(result, CommentListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], Comment)
    assert result.data[0].content == "Looks good to approve."


def test_comments_create(mock_client):
    mock_client._responses["POST /v1/deals/1/comments"] = make_response(
        201, SAMPLE_COMMENT
    )

    result = mock_client.deals.comments.create(1, content="Looks good to approve.")

    assert isinstance(result, Comment)
    assert result.id == 10
    assert result.content == "Looks good to approve."


def test_comments_update(mock_client):
    updated = {**SAMPLE_COMMENT, "content": "Updated comment text"}
    mock_client._responses["PATCH /v1/deals/1/comments/10"] = make_response(
        200, updated
    )

    result = mock_client.deals.comments.update(1, 10, content="Updated comment text")

    assert isinstance(result, Comment)
    assert result.content == "Updated comment text"


def test_comments_delete(mock_client):
    mock_client._responses["DELETE /v1/deals/1/comments/10"] = make_response(
        200, {"status": "ok", "message": "Comment deleted"}
    )

    result = mock_client.deals.comments.delete(1, 10)

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"


# ── Assignments tests ───────────────────────────────────────────────────────


def test_assignments_list(mock_client):
    mock_client._responses["GET /v1/deals/1/assignments"] = make_response(
        200, SAMPLE_ASSIGNMENT_LIST
    )

    result = mock_client.deals.assignments.list(1)

    assert isinstance(result, AssignmentListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], Assignment)
    assert result.data[0].role == "assignee"


def test_assignments_create(mock_client):
    mock_client._responses["POST /v1/deals/1/assignments"] = make_response(
        201, SAMPLE_ASSIGNMENT
    )

    result = mock_client.deals.assignments.create(1, user_id=5, role="assignee")

    assert isinstance(result, Assignment)
    assert result.user_id == 5
    assert result.deal_id == 1


def test_assignments_delete(mock_client):
    mock_client._responses["DELETE /v1/deals/1/assignments/5"] = make_response(
        200, {"status": "ok", "message": "Assignment removed"}
    )

    result = mock_client.deals.assignments.delete(1, 5)

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"


def test_assignments_my_deals(mock_client):
    mock_client._responses["GET /v1/me/assigned-deals"] = make_response(
        200, SAMPLE_ASSIGNED_DEALS
    )

    result = mock_client.deals.assignments.my_deals()

    assert isinstance(result, AssignedDealsResponse)
    assert len(result.data) == 1
    assert result.data[0].business_name == "Acme Trucking LLC"


# ── Document Requests tests ────────────────────────────────────────────────


def test_doc_requests_list(mock_client):
    mock_client._responses["GET /v1/deals/1/doc-requests"] = make_response(
        200, SAMPLE_DOC_REQUEST_LIST
    )

    result = mock_client.deals.doc_requests.list(1)

    assert isinstance(result, DocRequestListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], DocRequest)
    assert result.data[0].document_type == "bank_statement"


def test_doc_requests_create(mock_client):
    mock_client._responses["POST /v1/deals/1/doc-requests"] = make_response(
        201, SAMPLE_DOC_REQUEST
    )

    result = mock_client.deals.doc_requests.create(
        1,
        document_type="bank_statement",
        description="Need January 2026 statement",
        recipient_email="owner@acme.com",
    )

    assert isinstance(result, DocRequest)
    assert result.status == "pending"
    assert result.recipient_email == "owner@acme.com"


def test_doc_requests_update(mock_client):
    fulfilled = {
        **SAMPLE_DOC_REQUEST,
        "status": "received",
        "document_id": 15,
        "fulfilled_at": "2026-02-20T14:00:00",
    }
    mock_client._responses["PATCH /v1/deals/1/doc-requests/30"] = make_response(
        200, fulfilled
    )

    result = mock_client.deals.doc_requests.update(
        1, 30, status="received", document_id=15
    )

    assert isinstance(result, DocRequest)
    assert result.status == "received"
    assert result.document_id == 15


# ── Timeline tests ──────────────────────────────────────────────────────────


def test_deal_timeline(mock_client):
    mock_client._responses["GET /v1/deals/1/timeline"] = make_response(
        200, SAMPLE_TIMELINE
    )

    result = mock_client.deals.timeline.deal_timeline(1)

    assert isinstance(result, TimelineResponse)
    assert len(result.data) == 1
    assert result.data[0].event_type == "deal.created"
    assert result.meta.total == 1


def test_org_activity(mock_client):
    mock_client._responses["GET /v1/activity"] = make_response(200, SAMPLE_TIMELINE)

    result = mock_client.deals.timeline.org_activity()

    assert isinstance(result, TimelineResponse)
    assert len(result.data) == 1


# ── User Search tests ──────────────────────────────────────────────────────


def test_user_search(mock_client):
    mock_client._responses["GET /v1/users/search"] = make_response(
        200, SAMPLE_USER_SEARCH
    )

    result = mock_client.deals.users.search("analyst")

    assert isinstance(result, UserSearchResponse)
    assert len(result.data) == 1
    assert result.data[0].email == "analyst@banklyze.com"
    assert result.data[0].role == "analyst"
