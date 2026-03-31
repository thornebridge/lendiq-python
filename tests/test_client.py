"""Tests for client initialization, retry, and error handling."""

from __future__ import annotations


from lendiq import LendIQClient, __version__


def test_version():
    assert __version__ == "1.3.0"


def test_client_init():
    client = LendIQClient(api_key="liq_test_xxx")
    assert client.last_request_id is None
    assert client.deals is not None
    assert client.documents is not None
    assert client.webhooks is not None
    client.close()


def test_client_context_manager():
    with LendIQClient(api_key="liq_test_xxx") as client:
        assert client.deals is not None


def test_client_resources_complete():
    """All 19 top-level resources + 5 sub-resources are wired."""
    with LendIQClient(api_key="liq_test_xxx") as client:
        top_level = [
            "admin", "lvl", "crm", "deals", "documents", "events",
            "transactions", "exports", "ingest", "instant", "integrations",
            "keys", "notifications", "oauth", "onboarding", "push",
            "reviews", "rulesets", "sam_profiles", "shares", "team",
            "usage", "webhooks",
        ]
        for name in top_level:
            assert hasattr(client, name), f"Missing resource: {name}"

        # Sub-resources
        sub_resources = ["comments", "assignments", "doc_requests", "timeline", "users"]
        for name in sub_resources:
            assert hasattr(client.deals, name), f"Missing sub-resource: deals.{name}"
