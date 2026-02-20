"""Banklyze API resource modules."""

from banklyze.resources.deals import DealsResource
from banklyze.resources.documents import DocumentsResource
from banklyze.resources.exports import ExportsResource
from banklyze.resources.ingest import IngestResource
from banklyze.resources.rulesets import RulesetsResource
from banklyze.resources.transactions import TransactionsResource
from banklyze.resources.webhooks import WebhooksResource

__all__ = [
    "DealsResource",
    "DocumentsResource",
    "ExportsResource",
    "IngestResource",
    "RulesetsResource",
    "TransactionsResource",
    "WebhooksResource",
]
