# Banklyze Python SDK

Official Python client for the [Banklyze API](https://banklyze.com) — AI-powered MCA underwriting platform.

## Installation

```bash
pip install banklyze
```

## Quickstart

```python
from banklyze import BanklyzeClient

client = BanklyzeClient(api_key="bk_live_...", base_url="https://api.banklyze.com")

# Create a deal
deal = client.deals.create(business_name="Acme Trucking LLC", industry="Transportation")
print(deal["id"])

# Upload statements
client.statements.upload(deal["id"], "chase_jan_2026.pdf")

# Bulk upload
client.statements.upload_bulk(deal["id"], ["jan.pdf", "feb.pdf", "mar.pdf"])

# List deals
deals = client.deals.list(status="ready", page=1)
for d in deals["deals"]:
    print(d["business_name"], d["health_grade"])

# Get recommendation
rec = client.deals.recommendation(deal["id"])
print(rec["decision"], rec["paper_grade"])

# Export PDF report
pdf_bytes = client.exports.deal_pdf(deal["id"])
with open("report.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Context Manager

```python
with BanklyzeClient(api_key="bk_live_...") as client:
    deals = client.deals.list()
```

## Idempotency

Pass an idempotency key to prevent duplicate operations on retries:

```python
deal = client.deals.create(
    business_name="Acme Trucking LLC",
    idempotency_key="create-acme-001",
)
```

## Webhook Signature Verification

```python
from banklyze.webhooks import verify_signature

# In your webhook handler:
verify_signature(
    payload=request.body,
    signature=request.headers["X-Webhook-Signature"],
    secret="whsec_your_secret",
)
```

## Error Handling

```python
from banklyze import BanklyzeClient
from banklyze.exceptions import NotFoundError, RateLimitError, ValidationError

client = BanklyzeClient(api_key="bk_live_...")

try:
    deal = client.deals.get(999)
except NotFoundError:
    print("Deal not found")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Invalid request: {e}")
```
