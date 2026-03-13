"""Async deals resource — CRUD, decision, notes, recommendation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient
    from banklyze.pagination import AsyncPageIterator


class AsyncDealsResource:
    def __init__(self, client: AsyncBanklyzeClient):
        self._client = client

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
    ) -> dict[str, Any]:
        return await self._client._request(
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
    ) -> dict[str, Any]:
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

        return await self._client._request("POST", "/v1/deals", json=body, headers=headers or None)

    async def batch_create(
        self,
        deals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create multiple deals in a single request (max 50).

        Each element in ``deals`` must include ``business_name`` at minimum and
        may include any field accepted by :meth:`create`.
        """
        return await self._client._request("POST", "/v1/deals/batch", json=deals)

    async def get(self, deal_id: int) -> dict[str, Any]:
        return await self._client._request("GET", f"/v1/deals/{deal_id}")

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
    ) -> dict[str, Any]:
        """Update a deal — only provided fields are sent (PATCH semantics)."""
        fields: dict[str, Any] = {}
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
        for key, value in _all_fields.items():
            if value is not None:
                fields[key] = value
        return await self._client._request("PATCH", f"/v1/deals/{deal_id}", json=fields)

    async def delete(self, deal_id: int) -> dict[str, Any]:
        return await self._client._request("DELETE", f"/v1/deals/{deal_id}")

    async def stats(self) -> dict[str, Any]:
        """Aggregate KPI stats for the dashboard (total, by-status, avg health, volume)."""
        return await self._client._request("GET", "/v1/deals/stats")

    async def analytics(self) -> dict[str, Any]:
        """Portfolio analytics: approval rates, grade distribution, avg funding, etc."""
        return await self._client._request("GET", "/v1/deals/analytics")

    async def daily_stats(self, *, days: int = 30) -> dict[str, Any]:
        """Daily deal volume and approval rate trends for time-series charts.

        Args:
            days: Number of trailing days to return (7-90, default 30).
        """
        return await self._client._request(
            "GET",
            "/v1/deals/stats/daily",
            params={"days": days},
        )

    async def export_csv(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
    ) -> bytes:
        """Export deals as a CSV file.

        Returns the raw CSV bytes. Write to a file or decode as needed.
        """
        return await self._client._request(
            "GET",
            "/v1/deals/export/csv",
            params={"status": status, "q": q},
        )

    async def evaluate(
        self,
        deal_id: int,
        *,
        ruleset_id: int | None = None,
        ruleset_ids: list[int] | None = None,
    ) -> dict[str, Any]:
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
        return await self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/evaluate",
            params=params or None,
        )

    async def decision(
        self,
        deal_id: int,
        *,
        decision: str,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return await self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/decision",
            json={"decision": decision},
            headers=headers or None,
        )

    async def notes(self, deal_id: int, *, page: int = 1, per_page: int = 25) -> dict[str, Any]:
        return await self._client._request(
            "GET",
            f"/v1/deals/{deal_id}/notes",
            params={"page": page, "per_page": per_page},
        )

    async def add_note(
        self,
        deal_id: int,
        *,
        content: str,
        author: str = "API",
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return await self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/notes",
            json={"content": content, "author": author},
            headers=headers or None,
        )

    async def recommendation(self, deal_id: int) -> dict[str, Any]:
        return await self._client._request("GET", f"/v1/deals/{deal_id}/recommendation")

    async def regenerate_summary(
        self,
        deal_id: int,
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return await self._client._request(
            "POST",
            f"/v1/deals/{deal_id}/regenerate-summary",
            headers=headers or None,
        )

    def list_all(self, **filters: Any) -> AsyncPageIterator:
        """Iterate over all deals, auto-fetching pages."""
        from banklyze.pagination import AsyncPageIterator

        return AsyncPageIterator(self._client, "/v1/deals", data_key="deals", params=filters)
