"""Banklyze SDK response types.

All types are Pydantic models with ``extra="allow"`` for forward compatibility.
New API fields will be accepted without breaking existing SDK consumers.
"""

from banklyze.types.admin import (
    ErrorLogEntry,
    ErrorLogListResponse,
    UsageDailyEntry,
    UsageDailyResponse,
    UsageModelsEntry,
    UsageModelsResponse,
    UsageSummaryByEvent,
    UsageSummaryByModel,
    UsageSummaryResponse,
    UsageSummaryTotals,
)
from banklyze.types.auth import AuthLoginResponse
from banklyze.types.bvl import (
    BVLHardGate,
    BVLResult,
    BVLRun,
    BVLRunListResponse,
    BVLSignal,
    BVLStats,
    CallQueueLead,
    CallQueueResponse,
)
from banklyze.types.collaboration import (
    ActivityEvent,
    AssignedDealItem,
    AssignedDealsResponse,
    Assignment,
    AssignmentListResponse,
    Comment,
    CommentListResponse,
    DocRequest,
    DocRequestListResponse,
    TimelineResponse,
    UserSearchResponse,
    UserSearchResult,
)
from banklyze.types.common import ActionResponse, ErrorDetail, PaginationMeta
from banklyze.types.deal import (
    BusinessSummary,
    CoverageSummary,
    CrossDocDealSummary,
    DailyStatEntry,
    DailyStatsResponse,
    DealDetail,
    DealListResponse,
    DealNote,
    DealNotesListResponse,
    DealStats,
    DealSummary,
    ExistingDebtSummary,
    FinancialsSummary,
    HealthSummary,
    LargeDeposit,
    McaSummary,
    NsfOdSummary,
    OwnerSummary,
    PnLDealSummary,
    RecommendationSummary,
    ScreeningSummary,
    SelfReportedSummary,
    SourceSummary,
    TaxReturnDealSummary,
)
from banklyze.types.dlq import DlqActionResponse, DlqEntry, DlqListResponse
from banklyze.types.document import (
    AnalysisSummary,
    BatchDocumentStatusItem,
    BatchDocumentStatusResponse,
    BulkUploadItemResponse,
    BulkUploadResponse,
    DocumentDetail,
    DocumentListResponse,
    DocumentStatusResponse,
    DocumentSummary,
    DocumentUploadResponse,
)
from banklyze.types.event import SSEEvent
from banklyze.types.integration import (
    ApiHealth,
    Integration,
    IntegrationHealthResponse,
    QueueHealth,
    QuotaUsage,
    WebhookHealth,
)
from banklyze.types.ingest import (
    BatchDocumentStatus,
    BatchRecommendationSummary,
    BatchStatusResponse,
    IngestDocumentResult,
    IngestResponse,
)
from banklyze.types.key import APIKey, CreateKeyResponse, KeyListResponse
from banklyze.types.notification import (
    AllPreferencesResponse,
    Notification,
    NotificationListResponse,
    NotificationPreference,
    UnreadCountResponse,
)
from banklyze.types.ruleset import (
    ComparativeEvaluationResponse,
    Ruleset,
    RulesetEvaluation,
    RulesetListResponse,
)
from banklyze.types.share import ShareToken, ShareTokenListItem, ShareTokenListResponse
from banklyze.types.team import InviteResponse, TeamListResponse, TeamMember
from banklyze.types.transaction import (
    Transaction,
    TransactionCorrection,
    TransactionCorrectionListResponse,
    TransactionDetail,
    TransactionListResponse,
)
from banklyze.types.underwriting import Recommendation
from banklyze.types.usage import (
    DailyUsage,
    DocumentTypeUsage,
    ProcessingTimePercentiles,
    ProcessingTimeStats,
    UsageSummary,
)
from banklyze.types.webhook import (
    WebhookConfig,
    WebhookDelivery,
    WebhookDeliveryDetail,
    WebhookDeliveryListResponse,
    WebhookTestResult,
)

__all__ = [
    # Admin
    "ErrorLogEntry",
    "ErrorLogListResponse",
    "UsageDailyEntry",
    "UsageDailyResponse",
    "UsageModelsEntry",
    "UsageModelsResponse",
    "UsageSummaryByEvent",
    "UsageSummaryByModel",
    "UsageSummaryResponse",
    "UsageSummaryTotals",
    # Auth
    "AuthLoginResponse",
    # BVL
    "BVLHardGate",
    "BVLResult",
    "BVLRun",
    "BVLRunListResponse",
    "BVLSignal",
    "BVLStats",
    "CallQueueLead",
    "CallQueueResponse",
    # Collaboration
    "ActivityEvent",
    "AssignedDealItem",
    "AssignedDealsResponse",
    "Assignment",
    "AssignmentListResponse",
    "Comment",
    "CommentListResponse",
    "DocRequest",
    "DocRequestListResponse",
    "TimelineResponse",
    "UserSearchResponse",
    "UserSearchResult",
    # Common
    "ActionResponse",
    "ErrorDetail",
    "PaginationMeta",
    # Deal
    "BusinessSummary",
    "CoverageSummary",
    "CrossDocDealSummary",
    "DailyStatEntry",
    "DailyStatsResponse",
    "DealDetail",
    "DealListResponse",
    "DealNote",
    "DealNotesListResponse",
    "DealStats",
    "DealSummary",
    "ExistingDebtSummary",
    "FinancialsSummary",
    "HealthSummary",
    "LargeDeposit",
    "McaSummary",
    "NsfOdSummary",
    "OwnerSummary",
    "PnLDealSummary",
    "RecommendationSummary",
    "ScreeningSummary",
    "SelfReportedSummary",
    "SourceSummary",
    "TaxReturnDealSummary",
    # DLQ
    "DlqActionResponse",
    "DlqEntry",
    "DlqListResponse",
    # Document
    "AnalysisSummary",
    "BatchDocumentStatusItem",
    "BatchDocumentStatusResponse",
    "BulkUploadItemResponse",
    "BulkUploadResponse",
    "DocumentDetail",
    "DocumentListResponse",
    "DocumentStatusResponse",
    "DocumentSummary",
    "DocumentUploadResponse",
    # Event
    "SSEEvent",
    # Integration
    "ApiHealth",
    "Integration",
    "IntegrationHealthResponse",
    "QueueHealth",
    "QuotaUsage",
    "WebhookHealth",
    # Ingest
    "BatchDocumentStatus",
    "BatchRecommendationSummary",
    "BatchStatusResponse",
    "IngestDocumentResult",
    "IngestResponse",
    # Key
    "APIKey",
    "CreateKeyResponse",
    "KeyListResponse",
    # Notification
    "AllPreferencesResponse",
    "Notification",
    "NotificationListResponse",
    "NotificationPreference",
    "UnreadCountResponse",
    # Ruleset
    "ComparativeEvaluationResponse",
    "Ruleset",
    "RulesetEvaluation",
    "RulesetListResponse",
    # Share
    "ShareToken",
    "ShareTokenListItem",
    "ShareTokenListResponse",
    # Team
    "InviteResponse",
    "TeamListResponse",
    "TeamMember",
    # Transaction
    "Transaction",
    "TransactionCorrection",
    "TransactionCorrectionListResponse",
    "TransactionDetail",
    "TransactionListResponse",
    # Underwriting
    "Recommendation",
    # Usage
    "DailyUsage",
    "DocumentTypeUsage",
    "ProcessingTimePercentiles",
    "ProcessingTimeStats",
    "UsageSummary",
    # Webhook
    "WebhookConfig",
    "WebhookDelivery",
    "WebhookDeliveryDetail",
    "WebhookDeliveryListResponse",
    "WebhookTestResult",
]
