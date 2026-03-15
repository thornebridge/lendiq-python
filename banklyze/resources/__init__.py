"""Banklyze API resource modules."""

from banklyze.resources.admin import AdminResource, AsyncAdminResource
from banklyze.resources.bvl import AsyncBVLResource, BVLResource
from banklyze.resources.collaboration import (
    AssignmentsResource,
    AsyncAssignmentsResource,
    AsyncCommentsResource,
    AsyncDocRequestsResource,
    AsyncTimelineResource,
    AsyncUserSearchResource,
    CommentsResource,
    DocRequestsResource,
    TimelineResource,
    UserSearchResource,
)
from banklyze.resources.crm import AsyncCrmResource, CrmResource
from banklyze.resources.deals import DealsResource
from banklyze.resources.documents import AsyncDocumentsResource, DocumentsResource
from banklyze.resources.events import AsyncEventsResource, EventsResource
from banklyze.resources.exports import AsyncExportsResource, ExportsResource
from banklyze.resources.ingest import AsyncIngestResource, IngestResource
from banklyze.resources.integrations import AsyncIntegrationsResource, IntegrationsResource
from banklyze.resources.keys import AsyncKeysResource, KeysResource
from banklyze.resources.notifications import AsyncNotificationsResource, NotificationsResource
from banklyze.resources.oauth import AsyncOAuthResource, OAuthResource
from banklyze.resources.onboarding import AsyncOnboardingResource, OnboardingResource
from banklyze.resources.push import AsyncPushResource, PushResource
from banklyze.resources.rulesets import AsyncRulesetsResource, RulesetsResource
from banklyze.resources.share import AsyncSharesResource, SharesResource
from banklyze.resources.team import AsyncTeamResource, TeamResource
from banklyze.resources.transactions import AsyncTransactionsResource, TransactionsResource
from banklyze.resources.usage import AsyncUsageResource, UsageResource
from banklyze.resources.webhooks import AsyncWebhooksResource, WebhooksResource

__all__ = [
    # Admin
    "AdminResource",
    "AsyncAdminResource",
    # BVL
    "AsyncBVLResource",
    "BVLResource",
    # Collaboration
    "AssignmentsResource",
    "AsyncAssignmentsResource",
    "AsyncCommentsResource",
    "AsyncDocRequestsResource",
    "AsyncTimelineResource",
    "AsyncUserSearchResource",
    "CommentsResource",
    "DocRequestsResource",
    "TimelineResource",
    "UserSearchResource",
    # CRM
    "AsyncCrmResource",
    "CrmResource",
    # Core
    "AsyncDocumentsResource",
    "AsyncEventsResource",
    "AsyncExportsResource",
    "AsyncIngestResource",
    "AsyncIntegrationsResource",
    "AsyncKeysResource",
    "AsyncNotificationsResource",
    "AsyncOAuthResource",
    "AsyncOnboardingResource",
    "AsyncPushResource",
    "AsyncRulesetsResource",
    "AsyncSharesResource",
    "AsyncTeamResource",
    "AsyncTransactionsResource",
    "AsyncUsageResource",
    "AsyncWebhooksResource",
    "DealsResource",
    "DocumentsResource",
    "EventsResource",
    "ExportsResource",
    "IngestResource",
    "IntegrationsResource",
    "KeysResource",
    "NotificationsResource",
    "OAuthResource",
    "OnboardingResource",
    "PushResource",
    "RulesetsResource",
    "SharesResource",
    "TeamResource",
    "TransactionsResource",
    "UsageResource",
    "WebhooksResource",
]
