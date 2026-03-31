"""LendIQ API resource modules."""

from lendiq.resources.admin import AdminResource, AsyncAdminResource
from lendiq.resources.lvl import AsyncLVLResource, LVLResource
from lendiq.resources.collaboration import (
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
from lendiq.resources.crm import AsyncCrmResource, CrmResource
from lendiq.resources.deals import DealsResource
from lendiq.resources.documents import AsyncDocumentsResource, DocumentsResource
from lendiq.resources.events import AsyncEventsResource, EventsResource
from lendiq.resources.exports import AsyncExportsResource, ExportsResource
from lendiq.resources.ingest import AsyncIngestResource, IngestResource
from lendiq.resources.integrations import AsyncIntegrationsResource, IntegrationsResource
from lendiq.resources.keys import AsyncKeysResource, KeysResource
from lendiq.resources.notifications import AsyncNotificationsResource, NotificationsResource
from lendiq.resources.oauth import AsyncOAuthResource, OAuthResource
from lendiq.resources.onboarding import AsyncOnboardingResource, OnboardingResource
from lendiq.resources.push import AsyncPushResource, PushResource
from lendiq.resources.rulesets import AsyncRulesetsResource, RulesetsResource
from lendiq.resources.sam_profiles import AsyncSAMProfilesResource, SAMProfilesResource
from lendiq.resources.share import AsyncSharesResource, SharesResource
from lendiq.resources.team import AsyncTeamResource, TeamResource
from lendiq.resources.transactions import AsyncTransactionsResource, TransactionsResource
from lendiq.resources.usage import AsyncUsageResource, UsageResource
from lendiq.resources.webhooks import AsyncWebhooksResource, WebhooksResource

__all__ = [
    # Admin
    "AdminResource",
    "AsyncAdminResource",
    # LVL
    "AsyncLVLResource",
    "LVLResource",
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
    "AsyncSAMProfilesResource",
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
    "SAMProfilesResource",
    "SharesResource",
    "TeamResource",
    "TransactionsResource",
    "UsageResource",
    "WebhooksResource",
]
