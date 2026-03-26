"""Banklyze SDK response types.

All types are Pydantic models with ``extra="allow"`` for forward compatibility.
New API fields will be accepted without breaking existing SDK consumers.
"""

from banklyze.types.admin import (
    ErrorLogEntry,
    ErrorLogListResponse,
    HealthResponse,
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
    SAMEntity,
    SAMEntityListResponse,
    SAMStatsResponse,
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
from banklyze.types.common import ActionResponse, ErrorDetail, HealthFactor, PaginationMeta, ValidationDiscrepancy
from banklyze.types.crm import (
    CRMConfigResponse,
    FieldMappingResponse,
    SyncLogEntry,
    SyncLogResponse,
    SyncTriggerResponse,
    ConnectionTestResponse,
)
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
    DealAnalyticsResponse,
)
from banklyze.types.dlq import DlqActionResponse, DlqEntry, DlqListResponse
from banklyze.types.document import (
    AnalysisSummary,
    BatchDocumentStatusItem,
    BatchDocumentStatusResponse,
    BulkUploadItemResponse,
    BulkUploadResponse,
    DocumentDetail,
    DocumentIntegrity,
    DocumentListResponse,
    DocumentStatusResponse,
    DocumentSummary,
    DocumentUploadResponse,
    ExtractionConfidenceDetail,
    FieldConfidence,
    PrescreenSummary,
)
from banklyze.types.event import SSEEvent
from banklyze.types.instant import (
    ExpenseCategory,
    FeedbackResponse,
    InstantAnalysisResponse,
    InstantFileResult,
    InstantSummary,
    MCAPosition,
    PositionCompliance,
)
from banklyze.types.integration import (
    ApiHealth,
    Integration,
    IntegrationHealthResponse,
    IntegrationTestResponse,
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
from banklyze.types.oauth import OAuthTokenResponse
from banklyze.types.notification import (
    AllPreferencesResponse,
    Notification,
    NotificationListResponse,
    NotificationPreference,
    UnreadCountResponse,
)
from banklyze.types.push import PushStatusResponse, VapidKeyResponse
from banklyze.types.reviews import (
    ReviewActionResponse,
    ReviewDetailResponse,
    ReviewListItem,
    ReviewListResponse,
    TransactionReviewItem,
)
from banklyze.types.ruleset import (
    ComparativeEvaluationResponse,
    Ruleset,
    RulesetEvaluation,
    RulesetListResponse,
)
from banklyze.types.sam_profile import (
    SAMFetchRun,
    SAMFetchRunListResponse,
    SAMProfileWatcher,
    SAMSearchProfile,
    SAMSearchProfileListResponse,
)
from banklyze.types.share import ShareToken, ShareTokenListItem, ShareTokenListResponse
from banklyze.types.team import InviteResponse, TeamListResponse, TeamMember
from banklyze.types.triage import (
    ConcatenationSignal,
    DocumentClassification,
    IntegrityCheck,
    QualityAssessment,
    TransactionSignals,
    TriagePageAnalysis,
    TriageRecommendation,
    TriageResponse,
)
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
    "HealthResponse",
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
    "SAMEntity",
    "SAMEntityListResponse",
    "SAMStatsResponse",
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
    "HealthFactor",
    "PaginationMeta",
    "ValidationDiscrepancy",
    # CRM
    "CRMConfigResponse",
    "FieldMappingResponse",
    "SyncLogEntry",
    "SyncLogResponse",
    "SyncTriggerResponse",
    "ConnectionTestResponse",
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
    "DealAnalyticsResponse",
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
    "DocumentIntegrity",
    "DocumentListResponse",
    "DocumentStatusResponse",
    "DocumentSummary",
    "DocumentUploadResponse",
    "ExtractionConfidenceDetail",
    "FieldConfidence",
    "PrescreenSummary",
    # Event
    "SSEEvent",
    # Instant
    "ExpenseCategory",
    "FeedbackResponse",
    "InstantAnalysisResponse",
    "InstantFileResult",
    "InstantSummary",
    "MCAPosition",
    "PositionCompliance",
    # Integration
    "ApiHealth",
    "Integration",
    "IntegrationHealthResponse",
    "IntegrationTestResponse",
    "QueueHealth",
    "QuotaUsage",
    "WebhookHealth",
    # Ingest
    "BatchDocumentStatus",
    "BatchRecommendationSummary",
    "BatchStatusResponse",
    "IngestDocumentResult",
    "IngestResponse",
    # OAuth
    "OAuthTokenResponse",
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
    # Push
    "PushStatusResponse",
    "VapidKeyResponse",
    # Review
    "ReviewActionResponse",
    "ReviewDetailResponse",
    "ReviewListItem",
    "ReviewListResponse",
    "TransactionReviewItem",
    # Ruleset
    "ComparativeEvaluationResponse",
    "Ruleset",
    "RulesetEvaluation",
    "RulesetListResponse",
    # SAM Profile
    "SAMFetchRun",
    "SAMFetchRunListResponse",
    "SAMProfileWatcher",
    "SAMSearchProfile",
    "SAMSearchProfileListResponse",
    # Share
    "ShareToken",
    "ShareTokenListItem",
    "ShareTokenListResponse",
    # Team
    "InviteResponse",
    "TeamListResponse",
    "TeamMember",
    # Triage
    "ConcatenationSignal",
    "DocumentClassification",
    "IntegrityCheck",
    "QualityAssessment",
    "TransactionSignals",
    "TriagePageAnalysis",
    "TriageRecommendation",
    "TriageResponse",
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
