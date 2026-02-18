"""Statements resource — upload, bulk upload, list, detail, status, reprocess, cancel."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.client import BanklyzeClient


class StatementsResource:
    def __init__(self, client: BanklyzeClient):
        self._client = client

    def upload(
        self,
        deal_id: int,
        file_path: str | Path,
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        p = Path(file_path)
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        with open(p, "rb") as f:
            return self._client._request(
                "POST",
                f"/v1/deals/{deal_id}/statements",
                files={"file": (p.name, f, "application/pdf")},
                headers=headers or None,
            )

    def upload_bulk(
        self,
        deal_id: int,
        file_paths: list[str | Path],
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        files = []
        handles = []
        try:
            for fp in file_paths:
                p = Path(fp)
                f = open(p, "rb")
                handles.append(f)
                files.append(("files", (p.name, f, "application/pdf")))
            return self._client._request(
                "POST",
                f"/v1/deals/{deal_id}/statements/bulk",
                files=files,
                headers=headers or None,
            )
        finally:
            for f in handles:
                f.close()

    def list(self, deal_id: int, *, page: int = 1, per_page: int = 25) -> dict[str, Any]:
        return self._client._request(
            "GET",
            f"/v1/deals/{deal_id}/statements",
            params={"page": page, "per_page": per_page},
        )

    def get(self, statement_id: int) -> dict[str, Any]:
        return self._client._request("GET", f"/v1/statements/{statement_id}")

    def status(self, statement_id: int) -> dict[str, Any]:
        return self._client._request("GET", f"/v1/statements/{statement_id}/status")

    def reprocess(self, statement_id: int, *, idempotency_key: str | None = None) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self._client._request(
            "POST",
            f"/v1/statements/{statement_id}/reprocess",
            headers=headers or None,
        )

    def cancel(self, statement_id: int, *, idempotency_key: str | None = None) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return self._client._request(
            "POST",
            f"/v1/statements/{statement_id}/cancel",
            headers=headers or None,
        )
