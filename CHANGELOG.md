# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-03-21

### Added

- **PrescreenSummary** — typed model for `DocumentDetail.prescreen` (was `dict | None`)
- **DocumentIntegrity** — typed model for `DocumentDetail.integrity` (was `dict | None`)
- **ExtractionConfidenceDetail** + **FieldConfidence** — typed model for `DocumentDetail.extraction_confidence_detail`
- **ValidationDiscrepancy** — typed model for `AnalysisSummary.validation_discrepancies` (was `list | None`)
- **HealthFactor** — typed model for `HealthSummary.factors` and `AnalysisSummary.health_factors_json` (was `dict | None`)
- **RecommendationSummary** — added `dscr`, `cash_flow_coverage_ratio`, `hypothetical_cfcr`, `hypothetical_dscr`, `stress_test_passed` fields

### Deprecated

- `AdminResource.get_constraints()` and `update_constraints()` now emit `DeprecationWarning`; use `client.rulesets` instead

### Fixed

- Version mismatch between `pyproject.toml` (1.1.0) and `__version__.py` (1.0.0) — both now 1.2.0

## [1.1.0] - 2026-03-20

### Added

- **HealthSummary** — documented `factors` dict structure: up to 12 sub-factors with `score`, `max`, `weight`, and `detail` keys
- **McaSummary** — added `mca_credit_score` (Layer 1 composite, bank-statement-only) and `credit_grade` fields
- **Recommendation** — added `hypothetical_cfcr` and `hypothetical_dscr` fields (projected ratios for declined deals), `mca_credit_score` field

### Changed

- Health score now uses 12 sub-factors aligned with underwriting Layer 1 (was 6)
- CFCR and DSCR are now populated on declined deals (previously null)
- MCA credit score isolated to Layer 1 — derived solely from bank statement data

## [1.0.0] - 2026-03-13

### Added

- **Typed responses** — all resource methods return Pydantic models with full IDE autocompletion
- **22 resource groups** covering the entire Banklyze API:
  - Core: deals, documents, transactions, exports, events, webhooks, ingest, rulesets
  - Collaboration: comments, assignments, doc requests, timeline, user search
  - Platform: team, notifications, keys, shares, usage, search
  - Admin: admin, integrations, onboarding
- **Sync + async clients** — `BanklyzeClient` and `AsyncBanklyzeClient`
- **Auto-pagination** — `list_all()` iterators on list endpoints
- **Retry with backoff** — exponential backoff with jitter, safe mutation handling
- **Webhook signature verification** — `verify_signature()` for HMAC-SHA256
- **SSE streaming** — real-time event streams for deals, org, and batches
- **Sub-resources** — `client.deals.comments.list(42)` for deal-scoped operations
- **PEP 561** — `py.typed` marker for type checker support
- **Forward compatible** — all response models use `extra="allow"`

### Changed

- Standardized all list response envelopes to `data` + `meta` (breaking change from 0.x)
- Switched build system from setuptools to hatchling
- Added pydantic as a required dependency
- Refactored sync client to use `ClientConfig` composition (eliminates duplicated retry logic)

### Removed

- Changed default `data_key` to `"data"` in pagination iterators (was entity-specific)
