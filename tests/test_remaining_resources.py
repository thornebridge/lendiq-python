"""Test remaining resources — webhooks config, keys, team, shares, notifications,
CRM, integrations, push, oauth, onboarding, LVL, SAM profiles, reviews, instant.

One or two tests per resource verifying the basic request pattern.
"""

from __future__ import annotations

import pytest

from lendiq.types.common import ActionResponse
from lendiq.types.crm import (
    CRMConfigResponse,
    FieldMappingResponse,
    SyncLogResponse,
    SyncTriggerResponse,
    ConnectionTestResponse,
)
from lendiq.types.integration import Integration, IntegrationHealthResponse, IntegrationTestResponse
from lendiq.types.key import CreateKeyResponse, KeyListResponse
from lendiq.types.notification import NotificationListResponse, UnreadCountResponse
from lendiq.types.oauth import OAuthTokenResponse
from lendiq.types.push import PushStatusResponse, VapidKeyResponse
from lendiq.types.reviews import ReviewActionResponse, ReviewDetailResponse, ReviewListResponse
from lendiq.types.share import ShareToken, ShareTokenListResponse
from lendiq.types.team import InviteResponse, TeamListResponse, TeamMember
from lendiq.types.webhook import (
    WebhookConfig,
    WebhookDeliveryListResponse,
    WebhookTestResult,
)
from tests.conftest import make_response


# ── Webhooks Config ─────────────────────────────────────────────────────────


def test_webhooks_get_config(mock_client):
    mock_client._responses["GET /v1/webhooks/config"] = make_response(
        200,
        {
            "url": "https://example.com/hook",
            "events": ["deal.created", "deal.approved"],
            "enabled": True,
            "has_secret": True,
        },
    )

    result = mock_client.webhooks.get_config()

    assert isinstance(result, WebhookConfig)
    assert result.url == "https://example.com/hook"
    assert result.enabled is True
    assert len(result.events) == 2


def test_webhooks_update_config(mock_client):
    mock_client._responses["PUT /v1/webhooks/config"] = make_response(
        200,
        {
            "url": "https://new.example.com/hook",
            "events": ["deal.created"],
            "enabled": True,
            "has_secret": True,
        },
    )

    result = mock_client.webhooks.update_config(
        url="https://new.example.com/hook",
        events=["deal.created"],
        secret="whsec_new",
    )

    assert isinstance(result, WebhookConfig)
    assert result.url == "https://new.example.com/hook"


def test_webhooks_delete_config(mock_client):
    mock_client._responses["DELETE /v1/webhooks/config"] = make_response(
        200, {"status": "ok", "message": "Webhook config deleted"}
    )

    result = mock_client.webhooks.delete_config()

    assert isinstance(result, ActionResponse)


def test_webhooks_test(mock_client):
    mock_client._responses["POST /v1/webhooks/test"] = make_response(
        200, {"delivered": True, "status_code": 200}
    )

    result = mock_client.webhooks.test()

    assert isinstance(result, WebhookTestResult)
    assert result.delivered is True


def test_webhooks_list_deliveries(mock_client):
    mock_client._responses["GET /v1/webhooks/deliveries"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "event_type": "deal.created",
                    "event_id": "evt_123",
                    "status_code": 200,
                    "success": True,
                    "created_at": "2026-02-01T10:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.webhooks.list_deliveries()

    assert isinstance(result, WebhookDeliveryListResponse)
    assert len(result.data) == 1
    assert result.data[0].success is True


# ── Keys ────────────────────────────────────────────────────────────────────


def test_keys_create(mock_client):
    mock_client._responses["POST /v1/keys"] = make_response(
        201,
        {
            "id": 1,
            "name": "Production Key",
            "key": "liq_live_xxxxxxxxxxxx",
            "key_prefix": "liq_live_xxxx",
            "scopes": "read,write",
            "expires_at": None,
            "created_at": "2026-02-01T10:00:00",
        },
    )

    result = mock_client.keys.create(name="Production Key")

    assert isinstance(result, CreateKeyResponse)
    assert result.key.startswith("liq_live_")
    assert result.name == "Production Key"


def test_keys_list(mock_client):
    mock_client._responses["GET /v1/keys"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "name": "Production Key",
                    "key_prefix": "liq_live_xxxx",
                    "scopes": "read,write",
                    "is_active": True,
                    "created_at": "2026-02-01T10:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.keys.list()

    assert isinstance(result, KeyListResponse)
    assert len(result.data) == 1


def test_keys_revoke(mock_client):
    mock_client._responses["DELETE /v1/keys/1"] = make_response(
        200, {"status": "ok", "message": "Key revoked"}
    )

    result = mock_client.keys.revoke(1)

    assert isinstance(result, ActionResponse)


# ── Team ────────────────────────────────────────────────────────────────────


def test_team_list(mock_client):
    mock_client._responses["GET /v1/team"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "email": "admin@lendiq.com",
                    "display_name": "Admin User",
                    "role": "admin",
                    "is_active": True,
                    "status": "active",
                    "created_at": "2026-01-01T00:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.team.list()

    assert isinstance(result, TeamListResponse)
    assert len(result.data) == 1
    assert result.data[0].role == "admin"


def test_team_invite(mock_client):
    mock_client._responses["POST /v1/team/invite"] = make_response(
        201,
        {
            "user_id": 10,
            "email": "new@lendiq.com",
            "role": "analyst",
            "invite_url": "https://app.lendiq.com/invite/xyz",
            "message": "Invitation sent",
        },
    )

    result = mock_client.team.invite(email="new@lendiq.com", role="analyst")

    assert isinstance(result, InviteResponse)
    assert result.email == "new@lendiq.com"
    assert result.role == "analyst"


def test_team_update(mock_client):
    mock_client._responses["PATCH /v1/team/10"] = make_response(
        200,
        {
            "id": 10,
            "email": "new@lendiq.com",
            "display_name": "New User",
            "role": "underwriter",
            "is_active": True,
            "status": "active",
            "created_at": "2026-02-01T00:00:00",
        },
    )

    result = mock_client.team.update(10, role="underwriter")

    assert isinstance(result, TeamMember)
    assert result.role == "underwriter"


def test_team_deactivate(mock_client):
    mock_client._responses["DELETE /v1/team/10"] = make_response(
        200, {"status": "ok", "message": "User deactivated"}
    )

    result = mock_client.team.deactivate(10)

    assert isinstance(result, ActionResponse)


# ── Shares ──────────────────────────────────────────────────────────────────


def test_shares_create(mock_client):
    mock_client._responses["POST /v1/deals/1/share"] = make_response(
        201,
        {
            "id": 1,
            "token": "sha_xxxxxxxxxxxx",
            "share_url": "https://app.lendiq.com/shared/sha_xxxxxxxxxxxx",
            "view_mode": "summary",
            "expires_at": "2026-03-01T00:00:00",
            "created_at": "2026-02-22T10:00:00",
        },
    )

    result = mock_client.shares.create(1)

    assert isinstance(result, ShareToken)
    assert result.view_mode == "summary"
    assert "shared" in result.share_url


def test_shares_list(mock_client):
    mock_client._responses["GET /v1/deals/1/shares"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "token": "sha_xxxxxxxxxxxx",
                    "share_url": "https://app.lendiq.com/shared/sha_xxxxxxxxxxxx",
                    "view_mode": "summary",
                    "is_active": True,
                    "access_count": 3,
                    "created_at": "2026-02-22T10:00:00",
                }
            ]
        },
    )

    result = mock_client.shares.list(1)

    assert isinstance(result, ShareTokenListResponse)
    assert len(result.data) == 1


def test_shares_revoke(mock_client):
    # revoke returns None (204-like), but mock returns 204 as empty dict
    mock_client._responses["DELETE /v1/deals/1/shares/1"] = make_response(204)

    # Should not raise
    mock_client.shares.revoke(1, 1)


# ── Notifications ───────────────────────────────────────────────────────────


def test_notifications_list(mock_client):
    mock_client._responses["GET /v1/notifications"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "notification_type": "deal.approved",
                    "status": "unread",
                    "title": "Deal Approved",
                    "body": "Acme Trucking LLC has been approved.",
                    "created_at": "2026-02-20T15:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.notifications.list()

    assert isinstance(result, NotificationListResponse)
    assert len(result.data) == 1
    assert result.data[0].notification_type == "deal.approved"


def test_notifications_unread_count(mock_client):
    mock_client._responses["GET /v1/notifications/unread-count"] = make_response(
        200, {"count": 5}
    )

    result = mock_client.notifications.unread_count()

    assert isinstance(result, UnreadCountResponse)
    assert result.count == 5


def test_notifications_mark_read(mock_client):
    mock_client._responses["POST /v1/notifications/mark-read"] = make_response(
        200, {"status": "ok", "message": "2 notifications marked as read"}
    )

    result = mock_client.notifications.mark_read([1, 2])

    assert isinstance(result, ActionResponse)


def test_notifications_mark_all_read(mock_client):
    mock_client._responses["POST /v1/notifications/mark-all-read"] = make_response(
        200, {"status": "ok", "message": "All notifications marked as read"}
    )

    result = mock_client.notifications.mark_all_read()

    assert isinstance(result, ActionResponse)


# ── CRM ─────────────────────────────────────────────────────────────────────


def test_crm_get_config(mock_client):
    mock_client._responses["GET /v1/crm/config/salesforce"] = make_response(
        200,
        {
            "provider": "salesforce",
            "enabled": True,
            "api_url": "https://acme.salesforce.com",
            "created_at": "2026-01-15T00:00:00",
        },
    )

    result = mock_client.crm.get_config("salesforce")

    assert isinstance(result, CRMConfigResponse)
    assert result.provider == "salesforce"
    assert result.enabled is True


def test_crm_test_connection(mock_client):
    mock_client._responses["POST /v1/crm/config/salesforce/test"] = make_response(
        200, {"success": True, "message": "Connection successful", "provider": "salesforce"}
    )

    result = mock_client.crm.test("salesforce")

    assert isinstance(result, ConnectionTestResponse)
    assert result.success is True


def test_crm_sync(mock_client):
    mock_client._responses["POST /v1/crm/sync"] = make_response(
        200, {"status": "queued", "message": "Sync triggered", "deal_id": 1}
    )

    result = mock_client.crm.sync(deal_id=1)

    assert isinstance(result, SyncTriggerResponse)
    assert result.status == "queued"


def test_crm_get_field_mapping(mock_client):
    mock_client._responses["GET /v1/crm/field-mapping/salesforce"] = make_response(
        200,
        {
            "provider": "salesforce",
            "mappings": {"business_name": "Account.Name"},
            "custom_fields": {},
        },
    )

    result = mock_client.crm.get_field_mapping("salesforce")

    assert isinstance(result, FieldMappingResponse)
    assert result.mappings["business_name"] == "Account.Name"


def test_crm_sync_log(mock_client):
    mock_client._responses["GET /v1/crm/sync-log"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "provider": "salesforce",
                    "deal_id": 1,
                    "direction": "outbound",
                    "status": "completed",
                    "created_at": "2026-02-20T10:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.crm.sync_log()

    assert isinstance(result, SyncLogResponse)
    assert len(result.data) == 1


# ── Integrations ────────────────────────────────────────────────────────────


def test_integrations_health(mock_client):
    mock_client._responses["GET /v1/integrations/health"] = make_response(
        200,
        {
            "webhooks": {"delivery_rate_24h": 99.5, "total_deliveries_24h": 50},
            "api": {"error_rate_24h": 0.5, "total_requests_24h": 200},
            "quota": {"documents_this_month": 150, "documents_limit": 500},
            "queue": {"active_pipelines": 2, "queue_depth": 0},
        },
    )

    result = mock_client.integrations.health()

    assert isinstance(result, IntegrationHealthResponse)
    assert result.webhooks.delivery_rate_24h == 99.5
    assert result.quota.documents_this_month == 150


def test_integrations_list(mock_client):
    mock_client._responses["GET /v1/integrations"] = make_response(
        200,
        {
            "integrations": [
                {
                    "integration_type": "slack",
                    "enabled": True,
                    "label": "Team Slack",
                    "has_credentials": True,
                }
            ]
        },
    )

    result = mock_client.integrations.list()

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Integration)
    assert result[0].integration_type == "slack"


def test_integrations_upsert(mock_client):
    mock_client._responses["PUT /v1/integrations/slack"] = make_response(
        200,
        {
            "integration_type": "slack",
            "enabled": True,
            "label": "Team Slack",
            "has_credentials": True,
        },
    )

    result = mock_client.integrations.upsert(
        "slack", enabled=True, label="Team Slack"
    )

    assert isinstance(result, Integration)
    assert result.enabled is True


# ── Push ────────────────────────────────────────────────────────────────────


def test_push_vapid_key(mock_client):
    mock_client._responses["GET /v1/push/vapid-key"] = make_response(
        200, {"public_key": "BN4dGgM_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
    )

    result = mock_client.push.vapid_key()

    assert isinstance(result, VapidKeyResponse)
    assert result.public_key.startswith("BN4dGgM")


def test_push_subscribe(mock_client):
    mock_client._responses["POST /v1/push/subscribe"] = make_response(
        200, {"status": "subscribed", "message": "Push subscription registered"}
    )

    result = mock_client.push.subscribe(
        endpoint="https://push.example.com/sub",
        keys={"p256dh": "xxx", "auth": "yyy"},
    )

    assert isinstance(result, PushStatusResponse)
    assert result.status == "subscribed"


# ── OAuth ───────────────────────────────────────────────────────────────────


def test_oauth_create_token(mock_client):
    mock_client._responses["POST /v1/oauth/token"] = make_response(
        200,
        {
            "access_token": "eyJhbGciOiJIUzI1NiJ9.xxxxx",
            "token_type": "bearer",
            "expires_in": 3600,
        },
    )

    result = mock_client.oauth.create_token(
        client_id="cli_xxxx", client_secret="sec_yyyy"
    )

    assert isinstance(result, OAuthTokenResponse)
    assert result.token_type == "bearer"
    assert result.expires_in == 3600


# ── Onboarding ──────────────────────────────────────────────────────────────


def test_onboarding_seed_demo(mock_client):
    mock_client._responses["POST /v1/onboarding/seed-demo"] = make_response(
        200, {"status": "ok", "message": "Demo data seeded"}
    )

    result = mock_client.onboarding.seed_demo()

    assert isinstance(result, ActionResponse)
    assert result.status == "ok"


# ── Reviews ─────────────────────────────────────────────────────────────────


def test_reviews_list(mock_client):
    mock_client._responses["GET /v1/reviews"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 15,
                    "deal_id": 1,
                    "filename": "chase_jan_2026.pdf",
                    "review_status": "needs_review",
                    "health_score": 65.0,
                    "transaction_count": 42,
                    "created_at": "2026-02-01T09:15:30",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.reviews.list()

    assert isinstance(result, ReviewListResponse)
    assert len(result.data) == 1
    assert result.data[0].review_status == "needs_review"


def test_reviews_get(mock_client):
    mock_client._responses["GET /v1/reviews/15"] = make_response(
        200,
        {
            "id": 15,
            "filename": "chase_jan_2026.pdf",
            "review_status": "needs_review",
            "opening_balance": 15000.0,
            "closing_balance": 18000.0,
            "transactions": [
                {
                    "id": 101,
                    "date": "2026-01-15",
                    "description": "ACH DEPOSIT - STRIPE",
                    "amount": 4500.0,
                    "transaction_type": "deposit",
                }
            ],
        },
    )

    result = mock_client.reviews.get(15)

    assert isinstance(result, ReviewDetailResponse)
    assert result.id == 15
    assert len(result.transactions) == 1


def test_reviews_approve(mock_client):
    mock_client._responses["POST /v1/reviews/15/approve"] = make_response(
        200,
        {"id": 15, "review_status": "approved", "message": "Review approved"},
    )

    result = mock_client.reviews.approve(15)

    assert isinstance(result, ReviewActionResponse)
    assert result.review_status == "approved"


def test_reviews_correct(mock_client):
    mock_client._responses["POST /v1/reviews/15/correct"] = make_response(
        200,
        {"id": 15, "review_status": "corrected", "message": "Corrections applied"},
    )

    result = mock_client.reviews.correct(
        15,
        corrections=[{"transaction_id": 101, "amount": 4600.0}],
        notes="Amount was slightly off",
    )

    assert isinstance(result, ReviewActionResponse)
    assert result.review_status == "corrected"


# ── LVL ─────────────────────────────────────────────────────────────────────


def test_lvl_list_runs(mock_client):
    from lendiq.types.lvl import LVLRunListResponse

    mock_client._responses["GET /v1/lvl/runs"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "status": "completed",
                    "total_leads": 50,
                    "validated": 48,
                    "failed": 2,
                    "created_at": "2026-02-20T10:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.lvl.list_runs()

    assert isinstance(result, LVLRunListResponse)
    assert len(result.data) == 1
    assert result.data[0].status == "completed"


def test_lvl_create_run(mock_client):
    from lendiq.types.lvl import LVLRun

    mock_client._responses["POST /v1/lvl/runs"] = make_response(
        201,
        {
            "id": 2,
            "status": "running",
            "total_leads": 30,
            "validated": 0,
            "failed": 0,
            "created_at": "2026-02-25T10:00:00",
        },
    )

    result = mock_client.lvl.create_run()

    assert isinstance(result, LVLRun)
    assert result.status == "running"


# ── SAM Profiles ────────────────────────────────────────────────────────────


def test_sam_profiles_list(mock_client):
    from lendiq.types.sam_profile import SAMSearchProfileListResponse

    mock_client._responses["GET /v1/sam/profiles"] = make_response(
        200,
        {
            "data": [
                {
                    "id": 1,
                    "name": "MCA Lenders",
                    "description": "Search for MCA lending opportunities",
                    "naics_codes": ["522390"],
                    "state_codes": ["NY", "CA"],
                    "sba_business_types": ["LLC"],
                    "min_suitability_score": 60,
                    "auto_create_deals": True,
                    "status": "active",
                    "schedule_hour_utc": 6,
                    "created_at": "2026-01-01T00:00:00",
                    "updated_at": "2026-01-01T00:00:00",
                }
            ],
            "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
        },
    )

    result = mock_client.sam_profiles.list()

    assert isinstance(result, SAMSearchProfileListResponse)
    assert len(result.data) == 1
    assert result.data[0].name == "MCA Lenders"


def test_sam_profiles_create(mock_client):
    from lendiq.types.sam_profile import SAMSearchProfile

    mock_client._responses["POST /v1/sam/profiles"] = make_response(
        201,
        {
            "id": 2,
            "name": "New Profile",
            "description": "Small business lending",
            "naics_codes": ["522310"],
            "state_codes": ["TX"],
            "sba_business_types": ["Corporation"],
            "min_suitability_score": 50,
            "auto_create_deals": False,
            "status": "active",
            "schedule_hour_utc": 8,
            "created_at": "2026-02-25T10:00:00",
            "updated_at": "2026-02-25T10:00:00",
        },
    )

    result = mock_client.sam_profiles.create(
        name="New Profile",
        naics_codes=["522310"],
        state_codes=["TX"],
    )

    assert isinstance(result, SAMSearchProfile)
    assert result.name == "New Profile"
