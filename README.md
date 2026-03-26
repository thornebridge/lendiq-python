<div align="center">
<br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://banklyze.com/icons/banklyze-mark-white.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://banklyze.com/icons/Banklyze-Logo.svg">
  <img alt="Banklyze" src="https://banklyze.com/icons/Banklyze-Logo.svg" width="36">
</picture>
&nbsp;&nbsp;
<samp><b>&nbsp;B &nbsp;A &nbsp;N &nbsp;K &nbsp;L &nbsp;Y &nbsp;Z &nbsp;E&nbsp;</b></samp>

<br />
<br />

### Upload a bank statement. Get an underwriting decision.

The official Python SDK for the Banklyze API.<br />
Turn months of manual underwriting into a single API call.

<br />

[![PyPI](https://img.shields.io/pypi/v/banklyze?style=flat-square&color=0a0a0a&labelColor=0a0a0a)](https://pypi.org/project/banklyze/)
&nbsp;
[![MIT](https://img.shields.io/badge/license-MIT-0a0a0a?style=flat-square&labelColor=0a0a0a)](LICENSE)
&nbsp;
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-0a0a0a?style=flat-square&labelColor=0a0a0a)](https://python.org)
&nbsp;
[![Typed](https://img.shields.io/badge/types-strict-0a0a0a?style=flat-square&labelColor=0a0a0a)](https://peps.python.org/pep-0561/)
&nbsp;
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-0a0a0a?style=flat-square&labelColor=0a0a0a)](https://docs.pydantic.dev)

<br />

[Get API Key](https://banklyze.com) &nbsp;&middot;&nbsp; [Documentation](https://docs.banklyze.com) &nbsp;&middot;&nbsp; [API Reference](https://docs.banklyze.com/api) &nbsp;&middot;&nbsp; [Discord](https://discord.gg/banklyze)

<br />
</div>

---

<br />

## 7 lines. That's it.

```python
from banklyze import BanklyzeClient

client = BanklyzeClient(api_key="bk_live_...")

deal = client.deals.create(business_name="Acme Trucking LLC")
client.documents.upload(deal.id, "statements/chase_jan.pdf")

result = client.deals.get(deal.id)
print(result.recommendation.decision)  # "approved"
```

That PDF just went through OCR extraction, LLM parsing, transaction screening, tamper detection, 12-factor health scoring, and a full underwriting recommendation. Your team didn't write a single rule.

<br />

## Why teams switch to Banklyze

<table>
<tr>
<td width="50%">

### Before Banklyze
- Manual PDF review (20-40 min per deal)
- Spreadsheet-based scoring
- Inconsistent underwriting criteria
- No tamper detection
- Weeks to onboard new data sources

</td>
<td width="50%">

### After Banklyze
- Automated analysis (seconds per deal)
- 12-factor composite health scoring
- Configurable rulesets with version history
- PDF integrity + tampering detection
- One API call to process any bank statement

</td>
</tr>
</table>

<br />

## Install

```bash
pip install banklyze
```

> Requires Python 3.10+. Only two dependencies: `httpx` and `pydantic`.

<br />

## Sync and async, your choice

Both clients have identical APIs. Pick the one that fits your stack.

```python
# Sync
with BanklyzeClient(api_key="bk_live_...") as client:
    deals = client.deals.list(status="ready")
```

```python
# Async
from banklyze import AsyncBanklyzeClient

async with AsyncBanklyzeClient(api_key="bk_live_...") as client:
    deals = await client.deals.list(status="ready")
```

<br />

## Everything is typed

Every method returns a Pydantic model. Not `dict`. Not `Any`. Real models with real autocompletion.

```python
detail = client.deals.get(deal_id)

# IDE knows every field, every nested object, every type
detail.health.health_score                     # float
detail.health.health_grade                     # str
detail.recommendation.decision                 # "approved" | "conditional" | "declined"
detail.recommendation.risk_factors             # list[str]
detail.recommendation.strengths                # list[str]
detail.financials.avg_monthly_deposits         # float
detail.mca.mca_credit_score                    # float | None

# 12 health sub-factors, individually scored and weighted
for name, factor in detail.health.factors.items():
    print(f"{name}: {factor.score}/{factor.max} (weight: {factor.weight})")
```

All response models are forward-compatible (`extra="allow"`). New API fields are accepted automatically — your code never breaks on deploy.

<br />

## Document intelligence, built in

Upload a PDF and get back structured intelligence — no OCR pipeline to build, no LLM prompts to tune.

```python
doc = client.documents.get(doc_id)

# Pre-screen (regex-based, instant, no LLM cost)
doc.prescreen.bank_name          # "Chase"
doc.prescreen.opening_balance    # 15420.00
doc.prescreen.viable             # True
doc.prescreen.confidence         # 0.95

# Tamper detection
doc.integrity.tampering_risk_level  # "clean" | "low" | "medium" | "high"
doc.integrity.tampering_flags       # list[str]

# Extraction confidence scoring
doc.extraction_confidence_detail.overall_confidence  # 0.94
doc.extraction_confidence_detail.overall_tier        # "HIGH"

# Cross-document validation
doc.analysis.validation_is_reliable       # True
doc.analysis.validation_discrepancies     # list[ValidationDiscrepancy]
```

<br />

## Instant analysis — no account required

Let prospects try Banklyze before they sign up. The instant endpoint processes a PDF in under 2 seconds with no data persistence.

```python
result = client.instant.analyze("statement.pdf")

print(result.summary.total_deposits)        # 284500.00
print(result.summary.total_mca_positions)   # 3
print(result.summary.avg_revenue_quality)   # 0.82

# Per-file breakdown
for file in result.results:
    print(file.bank_name, file.nsf_count, file.mca_daily_obligation)
```

<br />

## Real-time pipeline streaming

Watch documents process in real time. No polling.

```python
for event in client.events.stream(deal_id=deal_id):
    if event.event == "stage":
        print(f"Stage: {event.data}")  # "extracting_text" → "parsing" → "screening" → "scoring"
    elif event.event == "complete":
        print("Analysis complete")
```

<br />

## Auto-pagination

Forget page math. Iterate over thousands of records with a single loop.

```python
for deal in client.deals.list_all(status="ready"):
    print(deal.business_name, deal.health_grade)
    # Typed as DealSummary — full autocompletion
```

<br />

## Error handling that doesn't suck

Every error is a typed exception with the context you need to debug. No parsing strings.

```python
from banklyze.exceptions import NotFoundError, RateLimitError, ValidationError

try:
    client.deals.get(deal_id)
except NotFoundError:
    # e.status_code == 404
    pass
except RateLimitError as e:
    # e.retry_after — seconds until you can retry
    pass
except ValidationError as e:
    # e.body — full validation error details
    pass
# Every error has e.request_id for instant support correlation
```

<br />

## Webhook verification in one line

```python
from banklyze.webhooks import verify_signature

# HMAC-SHA256 with constant-time comparison. Timing attacks don't apply.
verify_signature(payload=body, signature=headers["X-Webhook-Signature"], secret="whsec_...")
```

<br />

## Built for production

<table>
<tr><td><strong>Automatic retries</strong></td><td>Exponential backoff with jitter. Honors <code>Retry-After</code>. Safe for mutations — POST/PUT/PATCH only retry on connection errors, never on HTTP status codes.</td></tr>
<tr><td><strong>Idempotency</strong></td><td>Pass an idempotency key on any write. Retry all you want.</td></tr>
<tr><td><strong>Request tracking</strong></td><td>Every request gets a UUID. Every error includes it. <code>client.last_request_id</code> is always available.</td></tr>
<tr><td><strong>Timeouts</strong></td><td>Sensible defaults per operation type. <code>TIMEOUT_READ</code> (10s), <code>TIMEOUT_WRITE</code> (30s), <code>TIMEOUT_UPLOAD</code> (120s), <code>TIMEOUT_REPORT</code> (300s).</td></tr>
<tr><td><strong>Forward compatible</strong></td><td>All models use <code>extra="allow"</code>. API updates never break your code.</td></tr>
<tr><td><strong>PEP 561</strong></td><td><code>py.typed</code> marker included. Full <code>mypy --strict</code> support.</td></tr>
</table>

<br />

## Configuration

```python
client = BanklyzeClient(
    api_key="bk_live_...",               # required
    base_url="https://api.banklyze.com", # default
    timeout=30.0,                         # default (seconds)
    max_retries=2,                        # default
    logger=logging.getLogger("banklyze"), # optional debug logging
)
```

<br />

## 25 resources. Full API coverage.

Every endpoint in the Banklyze API has a typed method in this SDK.

| | Resource | What it does |
|-|----------|-------------|
| **Core** | `client.deals` | CRUD, decision, evaluate, notes, stats, analytics, batch |
| | `client.documents` | Upload, bulk upload, status, reprocess, triage, classify |
| | `client.transactions` | List, correct, corrections history |
| | `client.exports` | Deal and document CSV/PDF exports |
| | `client.rulesets` | Underwriting criteria CRUD, versioned, set default |
| **Intelligence** | `client.instant` | Free-tier instant PDF analysis (sub-2s, no persistence) |
| | `client.bvl` | Business validation runs, call queue, SAM entities |
| | `client.sam_profiles` | SAM.gov search profiles, watchers, automated triggers |
| | `client.reviews` | Document review queue, approve/correct workflow |
| **Real-time** | `client.events` | SSE streams for deals, org events, batch progress |
| | `client.webhooks` | Webhook config, test, delivery logs, retry |
| | `client.notifications` | In-app notifications and preferences |
| | `client.push` | Web push subscriptions |
| **Platform** | `client.team` | Invite, update, deactivate members |
| | `client.keys` | API key management |
| | `client.shares` | Public deal share links |
| | `client.ingest` | Bulk CRM ingest with batch tracking |
| | `client.crm` | Provider config, field mapping, bidirectional sync |
| | `client.integrations` | Slack, Teams, SMTP notification channels |
| | `client.admin` | Health, usage, error logs, DLQ, pipeline settings |
| | `client.usage` | Metering and processing time analytics |
| | `client.oauth` | Client credentials token exchange |

**Plus 5 sub-resources on every deal:**

```python
client.deals.comments.list(deal_id)        # threaded discussion
client.deals.assignments.create(deal_id)   # assign reviewers
client.deals.doc_requests.create(deal_id)  # request missing docs
client.deals.timeline.list(deal_id)        # full activity history
client.deals.users.search(q="jane")        # find team members
```

<br />

## Retry behavior

| Method | Rate limit (429) | Server error (5xx) | Connection error |
|--------|:---:|:---:|:---:|
| GET / DELETE | Retry | Retry | Retry |
| POST / PUT / PATCH | &mdash; | &mdash; | Retry |

Exponential backoff with jitter. 0.5 s base, 30 s cap. Honors `Retry-After`.

<br />

## We ship fast

This SDK is actively maintained by the Banklyze engineering team. We release weekly, respond to issues within 24 hours, and treat SDK quality with the same rigor as our core platform.

If something isn't right, [open an issue](https://github.com/thornebridge/banklyze-python/issues). We'll fix it.

<br />

## License

MIT &mdash; use it however you want.

<br />

<div align="center">

**[Get your API key](https://banklyze.com)** and start analyzing statements in minutes.

<br />

Built with care by the [Banklyze](https://banklyze.com) team.

</div>
