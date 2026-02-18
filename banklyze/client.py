"""BanklyzeClient — Stripe-style API client."""

from __future__ import annotations

from typing import Any

import httpx

from banklyze.exceptions import (
    AuthenticationError,
    BanklyzeError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from banklyze.resources.deals import DealsResource
from banklyze.resources.exports import ExportsResource
from banklyze.resources.statements import StatementsResource
from banklyze.resources.transactions import TransactionsResource
from banklyze.resources.webhooks import WebhooksResource


class BanklyzeClient:
    """Banklyze API client.

    Usage::

        client = BanklyzeClient(api_key="bk_live_...", base_url="https://api.banklyze.com")
        deals = client.deals.list()

    Or as a context manager::

        with BanklyzeClient(api_key="bk_live_...") as client:
            deals = client.deals.list()
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.banklyze.com",
        timeout: float = 30.0,
    ):
        headers: dict[str, str] = {}
        if api_key:
            headers["X-API-Key"] = api_key

        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=headers,
            timeout=timeout,
        )

        self.deals = DealsResource(self)
        self.statements = StatementsResource(self)
        self.transactions = TransactionsResource(self)
        self.exports = ExportsResource(self)
        self.webhooks = WebhooksResource(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self) -> None:
        self._http.close()

    # ── Internal request helpers ─────────────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | None = None,
        params: dict | None = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
        raw: bool = False,
    ) -> Any:
        """Make an API request and return parsed JSON (or raw bytes if raw=True)."""
        resp = self._http.request(
            method,
            path,
            json=json,
            params={k: v for k, v in (params or {}).items() if v is not None},
            files=files,
            headers=headers,
        )

        if resp.status_code >= 400:
            self._raise_for_status(resp)

        if raw:
            return resp.content

        if resp.status_code == 204:
            return {}

        return resp.json()

    def _raise_for_status(self, resp: httpx.Response) -> None:
        try:
            body = resp.json()
        except Exception:
            body = {}

        message = body.get("error") or body.get("detail") or resp.text

        if resp.status_code == 401:
            raise AuthenticationError(message, status_code=401, body=body)
        if resp.status_code == 404:
            raise NotFoundError(message, status_code=404, body=body)
        if resp.status_code == 422:
            raise ValidationError(message, status_code=422, body=body)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", "60"))
            raise RateLimitError(message, retry_after=retry_after, status_code=429, body=body)

        raise BanklyzeError(message, status_code=resp.status_code, body=body)
