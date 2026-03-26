"""Test PageIterator — multi-page iteration, typed models, edge cases."""

from __future__ import annotations

import pytest

from banklyze.types.deal import DealSummary
from tests.conftest import SAMPLE_DEAL, make_response


def _page_response(items, *, page, total, total_pages, per_page=25):
    """Build a paginated API response dict."""
    return {
        "data": items,
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }


def test_single_page(mock_client):
    """Single page of results yields all items."""
    mock_client._responses["GET /v1/deals"] = make_response(
        200,
        _page_response([SAMPLE_DEAL], page=1, total=1, total_pages=1),
    )

    items = list(mock_client.deals.list_all())

    assert len(items) == 1
    assert isinstance(items[0], DealSummary)
    assert items[0].business_name == "Acme Trucking LLC"


def test_multi_page(mock_client):
    """Three pages of results; yields items from all pages in order."""
    deal_a = {**SAMPLE_DEAL, "id": 1, "business_name": "Alpha Inc"}
    deal_b = {**SAMPLE_DEAL, "id": 2, "business_name": "Beta LLC"}
    deal_c = {**SAMPLE_DEAL, "id": 3, "business_name": "Gamma Corp"}

    # The PageIterator sends requests with query params, but MockTransport
    # matches on path only. We need a custom handler to return different
    # responses per page.
    import httpx

    page_data = {
        1: _page_response([deal_a], page=1, total=3, total_pages=3, per_page=1),
        2: _page_response([deal_b], page=2, total=3, total_pages=3, per_page=1),
        3: _page_response([deal_c], page=3, total=3, total_pages=3, per_page=1),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if request.url.path == "/v1/deals" and page in page_data:
            return make_response(200, page_data[page])
        return make_response(404, {"error": "Not found"})

    transport = httpx.MockTransport(handler)
    mock_client._http = httpx.Client(
        transport=transport,
        base_url="https://test.banklyze.com",
        headers={"X-API-Key": "bk_test_xxx"},
    )

    items = list(mock_client.deals.list_all())

    assert len(items) == 3
    assert items[0].business_name == "Alpha Inc"
    assert items[1].business_name == "Beta LLC"
    assert items[2].business_name == "Gamma Corp"


def test_empty_first_page(mock_client):
    """Empty first page yields nothing."""
    mock_client._responses["GET /v1/deals"] = make_response(
        200,
        _page_response([], page=1, total=0, total_pages=0),
    )

    items = list(mock_client.deals.list_all())

    assert len(items) == 0


def test_stops_at_total_pages(mock_client):
    """Does not fetch beyond total_pages."""
    import httpx

    fetch_count = []

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        fetch_count.append(page)
        # Only 1 page total
        return make_response(
            200,
            _page_response([SAMPLE_DEAL], page=page, total=1, total_pages=1),
        )

    transport = httpx.MockTransport(handler)
    mock_client._http = httpx.Client(
        transport=transport,
        base_url="https://test.banklyze.com",
        headers={"X-API-Key": "bk_test_xxx"},
    )

    items = list(mock_client.deals.list_all())

    assert len(items) == 1
    assert len(fetch_count) == 1  # Only fetched page 1


def test_typed_iteration(mock_client):
    """With model=DealSummary, yields DealSummary instances."""
    mock_client._responses["GET /v1/deals"] = make_response(
        200,
        _page_response([SAMPLE_DEAL], page=1, total=1, total_pages=1),
    )

    items = list(mock_client.deals.list_all())

    for item in items:
        assert isinstance(item, DealSummary)
        assert hasattr(item, "id")
        assert hasattr(item, "business_name")


def test_untyped_iteration(mock_client):
    """Without model, PageIterator yields raw dicts."""
    from banklyze.pagination import PageIterator

    mock_client._responses["GET /v1/deals"] = make_response(
        200,
        _page_response([SAMPLE_DEAL], page=1, total=1, total_pages=1),
    )

    items = list(PageIterator(mock_client, "/v1/deals"))

    assert len(items) == 1
    assert isinstance(items[0], dict)
    assert items[0]["business_name"] == "Acme Trucking LLC"
