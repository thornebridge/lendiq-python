"""LendIQ SDK response types.

All types are Pydantic models with ``extra="allow"`` for forward compatibility.
New API fields will be accepted without breaking existing SDK consumers.
"""

from lendiq.types.admin import (
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
from lendiq.types.auth import AuthLoginResponse
from lendiq.types.lvl import (
    LVLHardGate,
    LVLResult,
    LVLRun,
    LVLRunListResponse,
    LVLSignal,
    LVLStats,
    CallQueueLead,
    CallQueueResponse,
    SAMEntity,
    SAMEntityListResponse,
    SAMStatsResponse,
)
from lendiq.types.collaboration import (
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
from lendiq.types.common import ActionResponse, ErrorDetail, HealthFactor, PaginationMeta, ValidationDiscrepancy
from lendiq.types.crm import (
    CRMConfigResponse,
    FieldMappingResponse,
    SyncLogEntry,
    SyncLogResponse,
    SyncTriggerResponse,
    ConnectionTestResponse,
)
from lendiq.types.deal import (
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
from lendiq.types.dlq import DlqActionResponse, DlqEntry, DlqListResponse
from lendiq.types.document import (
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
    DocumentType,
    DocumentUploadResponse,
    DriverLicenseAnalysis,
    ExtractionConfidenceDetail,
    ExtractionMethod,
    FieldConfidence,
    PrescreenSummary,
    ProcessingStatus,
    VoidedCheckAnalysis,
)
from lendiq.types.event import SSEEvent
from lendiq.types.instant import (
    ExpenseCategory,
    FeedbackResponse,
    InstantAnalysisResponse,
    InstantFileResult,
    InstantSummary,
    MCAPosition,
    PositionCompliance,
)
from lendiq.types.integration import (
    ApiHealth,
    Integration,
    IntegrationHealthResponse,
    IntegrationTestResponse,
    QueueHealth,
    QuotaUsage,
    WebhookHealth,
)
from lendiq.types.ingest import (
    BatchDocumentStatus,
    BatchRecommendationSummary,
    BatchStatusResponse,
    IngestDocumentResult,
    IngestResponse,
)
from lendiq.types.key import APIKey, CreateKeyResponse, KeyListResponse
from lendiq.types.oauth import OAuthTokenResponse
from lendiq.types.notification import (
    AllPreferencesResponse,
    Notification,
    NotificationListResponse,
    NotificationPreference,
    UnreadCountResponse,
)
from lendiq.types.push import PushStatusResponse, VapidKeyResponse
from lendiq.types.reviews import (
    ReviewActionResponse,
    ReviewDetailResponse,
    ReviewListItem,
    ReviewListResponse,
    TransactionReviewItem,
)
from lendiq.types.ruleset import (
    ComparativeEvaluationResponse,
    Ruleset,
    RulesetEvaluation,
    RulesetListResponse,
)
from lendiq.types.sam_profile import (
    SAMFetchRun,
    SAMFetchRunListResponse,
    SAMProfileWatcher,
    SAMSearchProfile,
    SAMSearchProfileListResponse,
)
from lendiq.types.share import ShareToken, ShareTokenListItem, ShareTokenListResponse
from lendiq.types.team import InviteResponse, TeamListResponse, TeamMember
from lendiq.types.triage import (
    ConcatenationSignal,
    DocumentClassification,
    IntegrityCheck,
    QualityAssessment,
    TransactionSignals,
    TriagePageAnalysis,
    TriageRecommendation,
    TriageResponse,
)
from lendiq.types.transaction import (
    Transaction,
    TransactionCorrection,
    TransactionCorrectionListResponse,
    TransactionDetail,
    TransactionListResponse,
)
from lendiq.types.underwriting import Recommendation
from lendiq.types.usage import (
    DailyUsage,
    DocumentTypeUsage,
    ProcessingTimePercentiles,
    ProcessingTimeStats,
    UsageSummary,
)
from lendiq.types.webhook import (
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
    # LVL
    "LVLHardGate",
    "LVLResult",
    "LVLRun",
    "LVLRunListResponse",
    "LVLSignal",
    "LVLStats",
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
    "DocumentType",
    "DocumentUploadResponse",
    "DriverLicenseAnalysis",
    "ExtractionConfidenceDetail",
    "ExtractionMethod",
    "FieldConfidence",
    "PrescreenSummary",
    "ProcessingStatus",
    "VoidedCheckAnalysis",
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
