"""Deals resource — CRUD, decision, notes, recommendation.

Contains both synchronous (DealsResource) and asynchronous (AsyncDealsResource)
implementations. All methods return typed Pydantic models where applicable.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.common import ActionResponse
from banklyze.types.deal import (
    DailyStatsResponse,
    DealAnalyticsResponse,
    DealDetail,
    DealListResponse,
    DealNotesListResponse,
    DealNote,
    DealStats,
    DealSummary,
)
from banklyze.types.ruleset import ComparativeEvaluationResponse
from banklyze.types.underwriting import Recommendation

if TYPE_CHECKING:
    from banklyze.pagination import AsyncPageIterator, PageIterator


# ── Sync resource ────────────────────────────────────────────────────────────


class DealsResource(SyncAPIResource):

    # ── List / Search ────────────────────────────────────────────────────

    def list(
        self,
        *,
        status: str | None = None,
        search: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        page: int = 1,
        per_page: int = 25,
        health_grade: str | None = None,
        industry: str | None = None,
        source_type: str | None = None,
        min_funding: float | None = None,
        max_funding: float | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> DealListResponse:
        data = self._request(
            "GET",
            "/v1/deals",
            params={
                "status": status,
                "search": search,
                "sort": sort,
                "order": order,
                "page": page,
                "per_page": per_page,
                "health_grade": health_grade,
                "industry": industry,
                "source_type": source_type,
                "min_funding": min_funding,
                "max_funding": max_funding,
                "date_from": date_from,
                "date_to": date_to,
            },
        )
        return DealListResponse.model_validate(data)

    def list_all(self, **filters: Any) -> PageIterator[DealSummary]:
        """Iterate over all deals, auto-fetching pages.

        Accepts the same keyword filters as :meth:`list` (``status``,
        ``search``, ``sort``, ``order``, ``health_grade``, etc.).

        Usage::

            for deal in client.deals.list_all(status="ready"):
                print(deal.business_name)
        """
        from banklyze.pagination import PageIterator

        return PageIterator(
            self._client, "/v1/deals", model=DealSummary, params=filters
        )

    # ── Create ───────────────────────────────────────────────────────────

    def create(
        self,
        *,
        business_name: str,
        dba_name: str | None = None,
        owner_name: str | None = None,
        industry: str | None = None,
        funding_amount_requested: float | None = None,
        notes: str | None = None,
        # Business details
        entity_type: str | None = None,
        ein: str | None = None,
        business_start_date: str | None = None,
        business_address_street: str | None = None,
        business_address_city: str | None = None,
        business_address_state: str | None = None,
        business_address_zip: str | None = None,
        business_phone: str | None = None,
        business_email: str | None = None,
        website: str | None = None,
        # Owner / Principal
        owner_title: str | None = None,
        owner_phone: str | None = None,
        owner_email: str | None = None,
        ownership_pct: float | None = None,
        owner_ssn_last4: str | None = None,
        owner_dob: str | None = None,
        owner_credit_score: int | None = None,
        owner_address_street: str | None = None,
        owner_address_city: str | None = None,
        owner_address_state: str | None = None,
        owner_address_zip: str | None = None,
        # Self-reported financials
        use_of_funds: str | None = None,
        self_reported_monthly_revenue: float | None = None,
        self_reported_annual_revenue: float | None = None,
        monthly_credit_card_volume: float | None = None,
        monthly_rent: float | None = None,
        # Existing debt
        existing_mca_positions: int | None = None,
        existing_mca_balance: float | None = None,
        existing_lender_names: str | None = None,
        has_term_loan: bool | None = None,
        monthly_loan_payments: float | None = None,
        has_tax_lien: bool | None = None,
        has_judgment: bool | None = None,
        has_bankruptcy: bool | None = None,
        # Source / Broker
        source_type: str | None = None,
        broker_name: str | None = None,
        broker_company: str | None = None,
        broker_email: str | None = None,
        broker_phone: str | None = None,
        commission_pct: float | None = None,
        referral_source: str | None = None,
        idempotency_key: str | None = None,
    ) -> DealSummary:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        body: dict[str, Any] = {"business_name": business_name}
        _optional_fields = {
            "dba_name": dba_name,
            "owner_name": owner_name,
            "industry": industry,
            "funding_amount_requested": funding_amount_requested,
            "notes": notes,
            "entity_type": entity_type,
            "ein": ein,
            "business_start_date": business_start_date,
            "business_address_street": business_address_street,
            "business_address_city": business_address_city,
            "business_address_state": business_address_state,
            "business_address_zip": business_address_zip,
            "business_phone": business_phone,
            "business_email": business_email,
            "website": website,
            "owner_title": owner_title,
            "owner_phone": owner_phone,
            "owner_email": owner_email,
            "ownership_pct": ownership_pct,
            "owner_ssn_last4": owner_ssn_last4,
            "owner_dob": owner_dob,
            "owner_credit_score": owner_credit_score,
            "owner_address_street": owner_address_street,
            "owner_address_city": owner_address_city,
            "owner_address_state": owner_address_state,
            "owner_address_zip": owner_address_zip,
            "use_of_funds": use_of_funds,
            "self_reported_monthly_revenue": self_reported_monthly_revenue,
            "self_reported_annual_revenue": self_reported_annual_revenue,
            "monthly_credit_card_volume": monthly_credit_card_volume,
            "monthly_rent": monthly_rent,
            "existing_mca_positions": existing_mca_positions,
            "existing_mca_balance": existing_mca_balance,
            "existing_lender_names": existing_lender_names,
            "has_term_loan": has_term_loan,
            "monthly_loan_payments": monthly_loan_payments,
            "has_tax_lien": has_tax_lien,
            "has_judgment": has_judgment,
            "has_bankruptcy": has_bankruptcy,
            "source_type": source_type,
            "broker_name": broker_name,
            "broker_company": broker_company,
            "broker_email": broker_email,
            "broker_phone": broker_phone,
            "commission_pct": commission_pct,
            "referral_source": referral_source,
        }
        for key, value in _optional_fields.items():
            if value is not None:
                body[key] = value

        data = self._request("POST", "/v1/deals", json=body, headers=headers or None)
        return DealSummary.model_validate(data)

    def batch_create(
        self,
        deals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create multiple deals in a single request (max 50).

        Each element in ``deals`` must include ``business_name`` at minimum and
        may include any field accepted by :meth:`create`.
        """
        return self._request("POST", "/v1/deals/batch", json=deals)

    # ── Detail ───────────────────────────────────────────────────────────

    def get(self, deal_id: int) -> DealDetail:
        data = self._request("GET", f"/v1/deals/{deal_id}")
        return DealDetail.model_validate(data)

    # ── Update ───────────────────────────────────────────────────────────

    def update(
        self,
        deal_id: int,
        *,
        business_name: str | None = None,
        dba_name: str | None = None,
        owner_name: str | None = None,
        industry: str | None = None,
        funding_amount_requested: float | None = None,
        notes: str | None = None,
        # Business details
        entity_type: str | None = None,
        ein: str | None = None,
        business_start_date: str | None = None,
        business_address_street: str | None = None,
        business_address_city: str | None = None,
        business_address_state: str | None = None,
        business_address_zip: str | None = None,
        business_phone: str | None = None,
        business_email: str | None = None,
        website: str | None = None,
        # Owner / Principal
        owner_title: str | None = None,
        owner_phone: str | None = None,
        owner_email: str | None = None,
        ownership_pct: float | None = None,
        owner_ssn_last4: str | None = None,
        owner_dob: str | None = None,
        owner_credit_score: int | None = None,
        owner_address_street: str | None = None,
        owner_address_city: str | None = None,
        owner_address_state: str | None = None,
        owner_address_zip: str | None = None,
        # Self-reported financials
        use_of_funds: str | None = None,
        self_reported_monthly_revenue: float | None = None,
        self_reported_annual_revenue: float | None = None,
        monthly_credit_card_volume: float | None = None,
        monthly_rent: float | None = None,
        # Existing debt
        existing_mca_positions: int | None = None,
        existing_mca_balance: float | None = None,
        existing_lender_names: str | None = None,
        has_term_loan: bool | None = None,
        monthly_loan_payments: float | None = None,
        has_tax_lien: bool | None = None,
        has_judgment: bool | None = None,
        has_bankruptcy: bool | None = None,
        # Source / Broker
        source_type: str | None = None,
        broker_name: str | None = None,
        broker_company: str | None = None,
        broker_email: str | None = None,
        broker_phone: str | None = None,
        commission_pct: float | None = None,
        referral_source: str | None = None,
    ) -> DealSummary:
        """Update a deal — only provided fields are sent (PATCH semantics)."""
        _all_fields = {
            "business_name": business_name,
            "dba_name": dba_name,
            "owner_name": owner_name,
            "industry": industry,
            "funding_amount_requested": funding_amount_requested,
            "notes": notes,
            "entity_type": entity_type,
            "ein": ein,
            "business_start_date": business_start_date,
            "business_address_street": business_address_street,
            "business_address_city": business_address_city,
            "business_address_state": business_address_state,
            "business_address_zip": business_address_zip,
            "business_phone": business_phone,
            "business_email": business_email,
            "website": website,
            "owner_title": owner_title,
            "owner_phone": owner_phone,
            "owner_email": owner_email,
            "ownership_pct": ownership_pct,
            "owner_ssn_last4": owner_ssn_last4,
            "owner_dob": owner_dob,
            "owner_credit_score": owner_credit_score,
            "owner_address_street": owner_address_street,
            "owner_address_city": owner_address_city,
            "owner_address_state": owner_address_state,
            "owner_address_zip": owner_address_zip,
            "use_of_funds": use_of_funds,
            "self_reported_monthly_revenue": self_reported_monthly_revenue,
            "self_reported_annual_revenue": self_reported_annual_revenue,
            "monthly_credit_card_volume": monthly_credit_card_volume,
            "monthly_rent": monthly_rent,
            "existing_mca_positions": existing_mca_positions,
            "existing_mca_balance": existing_mca_balance,
            "existing_lender_names": existing_lender_names,
            "has_term_loan": has_term_loan,
            "monthly_loan_payments": monthly_loan_payments,
            "has_tax_lien": has_tax_lien,
            "has_judgment": has_judgment,
            "has_bankruptcy": has_bankruptcy,
            "source_type": source_type,
            "broker_name": broker_name,
            "broker_company": broker_company,
            "broker_email": broker_email,
            "broker_phone": broker_phone,
            "commission_pct": commission_pct,
            "referral_source": referral_source,
        }
        fields = {k: v for k, v in _all_fields.items() if v is not None}
        data = self._request("PATCH", f"/v1/deals/{deal_id}", json=fields)
        return DealSummary.model_validate(data)

    # ── Delete ───────────────────────────────────────────────────────────

    def delete(self, deal_id: int) -> ActionResponse:
        data = self._request("DELETE", f"/v1/deals/{deal_id}")
        return ActionResponse.model_validate(data)

    # ── Stats & Analytics ────────────────────────────────────────────────

    def stats(self) -> DealStats:
        """Aggregate KPI stats for the dashboard (total, by-status, avg health, volume)."""
        data = self._request("GET", "/v1/deals/stats")
        return DealStats.model_validate(data)

    def analytics(self) -> DealAnalyticsResponse:
        """Portfolio analytics: approval rates, grade distribution, avg funding, etc."""
        data = self._request("GET", "/v1/deals/analytics")
        return DealAnalyticsResponse.model_validate(data)

    def daily_stats(self, *, days: int = 30) -> DailyStatsResponse:
        """Daily deal volume and approval rate trends for time-series charts.

        Args:
            days: Number of trailing days to return (7--90, default 30).
        """
        data = self._request(
            "GET",
            "/v1/deals/stats/daily",
            params={"days": days},
        )
        return DailyStatsResponse.model_validate(data)

    # ── Export ────────────────────────────────────────────────────────────

    def export_csv(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
    ) -> bytes:
        """Export deals as a CSV file.

        Returns the raw CSV bytes. Write to a file or decode as needed.
        """
        return self._request(
            "GET",
            "/v1/deals/export/csv",
            params={"status": status, "q": q},
            raw=True,
        )

    # ── Evaluate ─────────────────────────────────────────────────────────

    def evaluate(
        self,
        deal_id: int,
        *,
        ruleset_id: int | None = None,
        ruleset_ids: list[int] | None = None,
    ) -> ComparativeEvaluationResponse:
        """Evaluate a deal against one or more rulesets.

        Args:
            deal_id: The deal to evaluate.
            ruleset_id: Evaluate against a single ruleset.
            ruleset_ids: Evaluate against multiple rulesets (comparative).

        Returns the comparative evaluation response including per-ruleset
        decisions and the best-fit recommendation.
        """
        params: dict[str, Any] = {}
        if ruleset_id is not None:
            params["ruleset_id"] = ruleset_id
        if ruleset_ids is not None:
            params["ruleset_ids"] = ruleset_ids
        data = self._request(
            "POST",
            f"/v1/deals/{deal_id}/evaluate",
            params=params or None,
        )
        return ComparativeEvaluationResponse.model_validate(data)

    # ── Decision ─────────────────────────────────────────────────────────

    def decision(
        self,
        deal_id: int,
        *,
        decision: str,
        idempotency_key: str | None = None,
    ) -> ActionResponse:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = self._request(
            "POST",
            f"/v1/deals/{deal_id}/decision",
            json={"decision": decision},
            headers=headers or None,
        )
        return ActionResponse.model_validate(data)

    # ── Notes ────────────────────────────────────────────────────────────

    def notes(self, deal_id: int, *, page: int = 1, per_page: int = 25) -> DealNotesListResponse:
        data = self._request(
            "GET",
            f"/v1/deals/{deal_id}/notes",
            params={"page": page, "per_page": per_page},
        )
        return DealNotesListResponse.model_validate(data)

    def add_note(
        self,
        deal_id: int,
        *,
        content: str,
        author: str = "API",
        idempotency_key: str | None = None,
    ) -> DealNote:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = self._request(
            "POST",
            f"/v1/deals/{deal_id}/notes",
            json={"content": content, "author": author},
            headers=headers or None,
        )
        return DealNote.model_validate(data)

    # ── Recommendation ───────────────────────────────────────────────────

    def recommendation(self, deal_id: int) -> Recommendation:
        data = self._request("GET", f"/v1/deals/{deal_id}/recommendation")
        return Recommendation.model_validate(data)

    # ── Regenerate Summary ───────────────────────────────────────────────

    def regenerate_summary(
        self,
        deal_id: int,
        *,
        idempotency_key: str | None = None,
    ) -> ActionResponse:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = self._request(
            "POST",
            f"/v1/deals/{deal_id}/regenerate-summary",
            headers=headers or None,
        )
        return ActionResponse.model_validate(data)

    # ── Quick Start ───────────────────────────────────────────────────────

    def quick_start(
        self,
        *,
        business_name: str,
        file_path: str | Path,
        document_type: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a deal and upload a document in one request.

        Returns a dict with ``deal_id``, ``document_id``, ``status``, and
        ``message`` keys.
        """
        p = Path(file_path)
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        with open(p, "rb") as f:
            return self._request(
                "POST",
                "/v1/deals/quick-start",
                data={"business_name": business_name, **({"document_type": document_type} if document_type else {})},
                files={"file": (p.name, f, "application/pdf")},
                headers=headers or None,
                timeout=self._client.TIMEOUT_UPLOAD,
            )

    # ── Reprocess Failed ─────────────────────────────────────────────────

    def reprocess_failed(self, deal_id: int) -> ActionResponse:
        """Reprocess all failed or cancelled documents for a deal."""
        data = self._request("POST", f"/v1/deals/{deal_id}/reprocess-failed")
        return ActionResponse.model_validate(data)


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncDealsResource(AsyncAPIResource):

    # ── List / Search ────────────────────────────────────────────────────

    async def list(
        self,
        *,
        status: str | None = None,
        search: str | None = None,
        sort: str | None = None,
        order: str | None = None,
        page: int = 1,
        per_page: int = 25,
        health_grade: str | None = None,
        industry: str | None = None,
        source_type: str | None = None,
        min_funding: float | None = None,
        max_funding: float | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> DealListResponse:
        data = await self._request(
            "GET",
            "/v1/deals",
            params={
                "status": status,
                "search": search,
                "sort": sort,
                "order": order,
                "page": page,
                "per_page": per_page,
                "health_grade": health_grade,
                "industry": industry,
                "source_type": source_type,
                "min_funding": min_funding,
                "max_funding": max_funding,
                "date_from": date_from,
                "date_to": date_to,
            },
        )
        return DealListResponse.model_validate(data)

    def list_all(self, **filters: Any) -> AsyncPageIterator[DealSummary]:
        """Iterate over all deals, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(self._client, "/v1/deals", model=DealSummary, params=filters)

    # ── Create ───────────────────────────────────────────────────────────

    async def create(
        self,
        *,
        business_name: str,
        dba_name: str | None = None,
        owner_name: str | None = None,
        industry: str | None = None,
        funding_amount_requested: float | None = None,
        notes: str | None = None,
        # Business details
        entity_type: str | None = None,
        ein: str | None = None,
        business_start_date: str | None = None,
        business_address_street: str | None = None,
        business_address_city: str | None = None,
        business_address_state: str | None = None,
        business_address_zip: str | None = None,
        business_phone: str | None = None,
        business_email: str | None = None,
        website: str | None = None,
        # Owner / Principal
        owner_title: str | None = None,
        owner_phone: str | None = None,
        owner_email: str | None = None,
        ownership_pct: float | None = None,
        owner_ssn_last4: str | None = None,
        owner_dob: str | None = None,
        owner_credit_score: int | None = None,
        owner_address_street: str | None = None,
        owner_address_city: str | None = None,
        owner_address_state: str | None = None,
        owner_address_zip: str | None = None,
        # Self-reported financials
        use_of_funds: str | None = None,
        self_reported_monthly_revenue: float | None = None,
        self_reported_annual_revenue: float | None = None,
        monthly_credit_card_volume: float | None = None,
        monthly_rent: float | None = None,
        # Existing debt
        existing_mca_positions: int | None = None,
        existing_mca_balance: float | None = None,
        existing_lender_names: str | None = None,
        has_term_loan: bool | None = None,
        monthly_loan_payments: float | None = None,
        has_tax_lien: bool | None = None,
        has_judgment: bool | None = None,
        has_bankruptcy: bool | None = None,
        # Source / Broker
        source_type: str | None = None,
        broker_name: str | None = None,
        broker_company: str | None = None,
        broker_email: str | None = None,
        broker_phone: str | None = None,
        commission_pct: float | None = None,
        referral_source: str | None = None,
        idempotency_key: str | None = None,
    ) -> DealSummary:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        body: dict[str, Any] = {"business_name": business_name}
        _optional_fields = {
            "dba_name": dba_name,
            "owner_name": owner_name,
            "industry": industry,
            "funding_amount_requested": funding_amount_requested,
            "notes": notes,
            "entity_type": entity_type,
            "ein": ein,
            "business_start_date": business_start_date,
            "business_address_street": business_address_street,
            "business_address_city": business_address_city,
            "business_address_state": business_address_state,
            "business_address_zip": business_address_zip,
            "business_phone": business_phone,
            "business_email": business_email,
            "website": website,
            "owner_title": owner_title,
            "owner_phone": owner_phone,
            "owner_email": owner_email,
            "ownership_pct": ownership_pct,
            "owner_ssn_last4": owner_ssn_last4,
            "owner_dob": owner_dob,
            "owner_credit_score": owner_credit_score,
            "owner_address_street": owner_address_street,
            "owner_address_city": owner_address_city,
            "owner_address_state": owner_address_state,
            "owner_address_zip": owner_address_zip,
            "use_of_funds": use_of_funds,
            "self_reported_monthly_revenue": self_reported_monthly_revenue,
            "self_reported_annual_revenue": self_reported_annual_revenue,
            "monthly_credit_card_volume": monthly_credit_card_volume,
            "monthly_rent": monthly_rent,
            "existing_mca_positions": existing_mca_positions,
            "existing_mca_balance": existing_mca_balance,
            "existing_lender_names": existing_lender_names,
            "has_term_loan": has_term_loan,
            "monthly_loan_payments": monthly_loan_payments,
            "has_tax_lien": has_tax_lien,
            "has_judgment": has_judgment,
            "has_bankruptcy": has_bankruptcy,
            "source_type": source_type,
            "broker_name": broker_name,
            "broker_company": broker_company,
            "broker_email": broker_email,
            "broker_phone": broker_phone,
            "commission_pct": commission_pct,
            "referral_source": referral_source,
        }
        for key, value in _optional_fields.items():
            if value is not None:
                body[key] = value

        data = await self._request("POST", "/v1/deals", json=body, headers=headers or None)
        return DealSummary.model_validate(data)

    async def batch_create(
        self,
        deals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create multiple deals in a single request (max 50).

        Each element in ``deals`` must include ``business_name`` at minimum and
        may include any field accepted by :meth:`create`.
        """
        return await self._request("POST", "/v1/deals/batch", json=deals)

    # ── Detail ───────────────────────────────────────────────────────────

    async def get(self, deal_id: int) -> DealDetail:
        data = await self._request("GET", f"/v1/deals/{deal_id}")
        return DealDetail.model_validate(data)

    # ── Update ───────────────────────────────────────────────────────────

    async def update(
        self,
        deal_id: int,
        *,
        business_name: str | None = None,
        dba_name: str | None = None,
        owner_name: str | None = None,
        industry: str | None = None,
        funding_amount_requested: float | None = None,
        notes: str | None = None,
        # Business details
        entity_type: str | None = None,
        ein: str | None = None,
        business_start_date: str | None = None,
        business_address_street: str | None = None,
        business_address_city: str | None = None,
        business_address_state: str | None = None,
        business_address_zip: str | None = None,
        business_phone: str | None = None,
        business_email: str | None = None,
        website: str | None = None,
        # Owner / Principal
        owner_title: str | None = None,
        owner_phone: str | None = None,
        owner_email: str | None = None,
        ownership_pct: float | None = None,
        owner_ssn_last4: str | None = None,
        owner_dob: str | None = None,
        owner_credit_score: int | None = None,
        owner_address_street: str | None = None,
        owner_address_city: str | None = None,
        owner_address_state: str | None = None,
        owner_address_zip: str | None = None,
        # Self-reported financials
        use_of_funds: str | None = None,
        self_reported_monthly_revenue: float | None = None,
        self_reported_annual_revenue: float | None = None,
        monthly_credit_card_volume: float | None = None,
        monthly_rent: float | None = None,
        # Existing debt
        existing_mca_positions: int | None = None,
        existing_mca_balance: float | None = None,
        existing_lender_names: str | None = None,
        has_term_loan: bool | None = None,
        monthly_loan_payments: float | None = None,
        has_tax_lien: bool | None = None,
        has_judgment: bool | None = None,
        has_bankruptcy: bool | None = None,
        # Source / Broker
        source_type: str | None = None,
        broker_name: str | None = None,
        broker_company: str | None = None,
        broker_email: str | None = None,
        broker_phone: str | None = None,
        commission_pct: float | None = None,
        referral_source: str | None = None,
    ) -> DealSummary:
        """Update a deal — only provided fields are sent (PATCH semantics)."""
        _all_fields = {
            "business_name": business_name,
            "dba_name": dba_name,
            "owner_name": owner_name,
            "industry": industry,
            "funding_amount_requested": funding_amount_requested,
            "notes": notes,
            "entity_type": entity_type,
            "ein": ein,
            "business_start_date": business_start_date,
            "business_address_street": business_address_street,
            "business_address_city": business_address_city,
            "business_address_state": business_address_state,
            "business_address_zip": business_address_zip,
            "business_phone": business_phone,
            "business_email": business_email,
            "website": website,
            "owner_title": owner_title,
            "owner_phone": owner_phone,
            "owner_email": owner_email,
            "ownership_pct": ownership_pct,
            "owner_ssn_last4": owner_ssn_last4,
            "owner_dob": owner_dob,
            "owner_credit_score": owner_credit_score,
            "owner_address_street": owner_address_street,
            "owner_address_city": owner_address_city,
            "owner_address_state": owner_address_state,
            "owner_address_zip": owner_address_zip,
            "use_of_funds": use_of_funds,
            "self_reported_monthly_revenue": self_reported_monthly_revenue,
            "self_reported_annual_revenue": self_reported_annual_revenue,
            "monthly_credit_card_volume": monthly_credit_card_volume,
            "monthly_rent": monthly_rent,
            "existing_mca_positions": existing_mca_positions,
            "existing_mca_balance": existing_mca_balance,
            "existing_lender_names": existing_lender_names,
            "has_term_loan": has_term_loan,
            "monthly_loan_payments": monthly_loan_payments,
            "has_tax_lien": has_tax_lien,
            "has_judgment": has_judgment,
            "has_bankruptcy": has_bankruptcy,
            "source_type": source_type,
            "broker_name": broker_name,
            "broker_company": broker_company,
            "broker_email": broker_email,
            "broker_phone": broker_phone,
            "commission_pct": commission_pct,
            "referral_source": referral_source,
        }
        fields = {k: v for k, v in _all_fields.items() if v is not None}
        data = await self._request("PATCH", f"/v1/deals/{deal_id}", json=fields)
        return DealSummary.model_validate(data)

    # ── Delete ───────────────────────────────────────────────────────────

    async def delete(self, deal_id: int) -> ActionResponse:
        data = await self._request("DELETE", f"/v1/deals/{deal_id}")
        return ActionResponse.model_validate(data)

    # ── Stats & Analytics ────────────────────────────────────────────────

    async def stats(self) -> DealStats:
        """Aggregate KPI stats for the dashboard (total, by-status, avg health, volume)."""
        data = await self._request("GET", "/v1/deals/stats")
        return DealStats.model_validate(data)

    async def analytics(self) -> DealAnalyticsResponse:
        """Portfolio analytics: approval rates, grade distribution, avg funding, etc."""
        data = await self._request("GET", "/v1/deals/analytics")
        return DealAnalyticsResponse.model_validate(data)

    async def daily_stats(self, *, days: int = 30) -> DailyStatsResponse:
        """Daily deal volume and approval rate trends for time-series charts.

        Args:
            days: Number of trailing days to return (7-90, default 30).
        """
        data = await self._request(
            "GET",
            "/v1/deals/stats/daily",
            params={"days": days},
        )
        return DailyStatsResponse.model_validate(data)

    # ── Export ────────────────────────────────────────────────────────────

    async def export_csv(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
    ) -> bytes:
        """Export deals as a CSV file.

        Returns the raw CSV bytes. Write to a file or decode as needed.
        """
        return await self._request(
            "GET",
            "/v1/deals/export/csv",
            params={"status": status, "q": q},
            raw=True,
        )

    # ── Evaluate ─────────────────────────────────────────────────────────

    async def evaluate(
        self,
        deal_id: int,
        *,
        ruleset_id: int | None = None,
        ruleset_ids: list[int] | None = None,
    ) -> ComparativeEvaluationResponse:
        """Evaluate a deal against one or more rulesets.

        Args:
            deal_id: The deal to evaluate.
            ruleset_id: Evaluate against a single ruleset.
            ruleset_ids: Evaluate against multiple rulesets (comparative).

        Returns the comparative evaluation response including per-ruleset
        decisions and the best-fit recommendation.
        """
        params: dict[str, Any] = {}
        if ruleset_id is not None:
            params["ruleset_id"] = ruleset_id
        if ruleset_ids is not None:
            params["ruleset_ids"] = ruleset_ids
        data = await self._request(
            "POST",
            f"/v1/deals/{deal_id}/evaluate",
            params=params or None,
        )
        return ComparativeEvaluationResponse.model_validate(data)

    # ── Decision ─────────────────────────────────────────────────────────

    async def decision(
        self,
        deal_id: int,
        *,
        decision: str,
        idempotency_key: str | None = None,
    ) -> ActionResponse:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = await self._request(
            "POST",
            f"/v1/deals/{deal_id}/decision",
            json={"decision": decision},
            headers=headers or None,
        )
        return ActionResponse.model_validate(data)

    # ── Notes ────────────────────────────────────────────────────────────

    async def notes(self, deal_id: int, *, page: int = 1, per_page: int = 25) -> DealNotesListResponse:
        data = await self._request(
            "GET",
            f"/v1/deals/{deal_id}/notes",
            params={"page": page, "per_page": per_page},
        )
        return DealNotesListResponse.model_validate(data)

    async def add_note(
        self,
        deal_id: int,
        *,
        content: str,
        author: str = "API",
        idempotency_key: str | None = None,
    ) -> DealNote:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = await self._request(
            "POST",
            f"/v1/deals/{deal_id}/notes",
            json={"content": content, "author": author},
            headers=headers or None,
        )
        return DealNote.model_validate(data)

    # ── Recommendation ───────────────────────────────────────────────────

    async def recommendation(self, deal_id: int) -> Recommendation:
        data = await self._request("GET", f"/v1/deals/{deal_id}/recommendation")
        return Recommendation.model_validate(data)

    # ── Regenerate Summary ───────────────────────────────────────────────

    async def regenerate_summary(
        self,
        deal_id: int,
        *,
        idempotency_key: str | None = None,
    ) -> ActionResponse:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = await self._request(
            "POST",
            f"/v1/deals/{deal_id}/regenerate-summary",
            headers=headers or None,
        )
        return ActionResponse.model_validate(data)

    # ── Quick Start ───────────────────────────────────────────────────────

    async def quick_start(
        self,
        *,
        business_name: str,
        file_path: str | Path,
        document_type: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a deal and upload a document in one request.

        Returns a dict with ``deal_id``, ``document_id``, ``status``, and
        ``message`` keys.
        """
        p = Path(file_path)
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        with open(p, "rb") as f:
            return await self._request(
                "POST",
                "/v1/deals/quick-start",
                data={"business_name": business_name, **({"document_type": document_type} if document_type else {})},
                files={"file": (p.name, f, "application/pdf")},
                headers=headers or None,
                timeout=self._client.TIMEOUT_UPLOAD,
            )

    # ── Reprocess Failed ─────────────────────────────────────────────────

    async def reprocess_failed(self, deal_id: int) -> ActionResponse:
        """Reprocess all failed or cancelled documents for a deal."""
        data = await self._request("POST", f"/v1/deals/{deal_id}/reprocess-failed")
        return ActionResponse.model_validate(data)
