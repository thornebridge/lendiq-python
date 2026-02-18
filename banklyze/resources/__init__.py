"""Banklyze API resource modules."""

from banklyze.resources.deals import DealsResource
from banklyze.resources.exports import ExportsResource
from banklyze.resources.statements import StatementsResource
from banklyze.resources.transactions import TransactionsResource
from banklyze.resources.webhooks import WebhooksResource

__all__ = [
    "DealsResource",
    "ExportsResource",
    "StatementsResource",
    "TransactionsResource",
    "WebhooksResource",
]
