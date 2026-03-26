"""Instant analysis resource — free-tier PDF analysis, no data persistence.

Contains both sync (InstantResource) and async (AsyncInstantResource) implementations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.common import ActionResponse
from banklyze.types.instant import FeedbackResponse, InstantAnalysisResponse


class InstantResource(SyncAPIResource):
    """Synchronous instant analysis resource."""

    def analyze(
        self,
        file_path: str | Path,
        *,
        vision_fallback: bool = False,
    ) -> InstantAnalysisResponse:
        """Upload a PDF for instant analysis (no data persisted).

        Args:
            file_path: Path to the PDF file.
            vision_fallback: Use vision LLM fallback for low-quality scans.
        """
        p = Path(file_path)
        params: dict[str, Any] = {}
        if vision_fallback:
            params["vision_fallback"] = True
        with open(p, "rb") as f:
            raw = self._request(
                "POST",
                "/v1/instant-analysis",
                files={"file": (p.name, f, "application/pdf")},
                params=params or None,
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        return InstantAnalysisResponse.model_validate(raw)

    def submit_feedback(
        self,
        *,
        session_id: str,
        filename: str,
        rating: str,
        issue_category: str | None = None,
        issue_detail: str | None = None,
    ) -> FeedbackResponse:
        """Submit feedback for an instant analysis result.

        Args:
            session_id: The session_id from the analysis response.
            filename: Which file the feedback is for.
            rating: ``"thumbs_up"`` or ``"thumbs_down"``.
            issue_category: Optional category (e.g. ``"wrong_deposits"``).
            issue_detail: Optional free-text detail.
        """
        body: dict[str, Any] = {
            "session_id": session_id,
            "filename": filename,
            "rating": rating,
        }
        if issue_category is not None:
            body["issue_category"] = issue_category
        if issue_detail is not None:
            body["issue_detail"] = issue_detail
        raw = self._request("POST", "/v1/instant-analysis-feedback", json=body)
        return FeedbackResponse.model_validate(raw)


class AsyncInstantResource(AsyncAPIResource):
    """Asynchronous instant analysis resource."""

    async def analyze(
        self,
        file_path: str | Path,
        *,
        vision_fallback: bool = False,
    ) -> InstantAnalysisResponse:
        """Upload a PDF for instant analysis (no data persisted).

        Args:
            file_path: Path to the PDF file.
            vision_fallback: Use vision LLM fallback for low-quality scans.
        """
        p = Path(file_path)
        params: dict[str, Any] = {}
        if vision_fallback:
            params["vision_fallback"] = True
        with open(p, "rb") as f:
            raw = await self._request(
                "POST",
                "/v1/instant-analysis",
                files={"file": (p.name, f, "application/pdf")},
                params=params or None,
                timeout=self._client.TIMEOUT_UPLOAD,
            )
        return InstantAnalysisResponse.model_validate(raw)

    async def submit_feedback(
        self,
        *,
        session_id: str,
        filename: str,
        rating: str,
        issue_category: str | None = None,
        issue_detail: str | None = None,
    ) -> FeedbackResponse:
        """Submit feedback for an instant analysis result."""
        body: dict[str, Any] = {
            "session_id": session_id,
            "filename": filename,
            "rating": rating,
        }
        if issue_category is not None:
            body["issue_category"] = issue_category
        if issue_detail is not None:
            body["issue_detail"] = issue_detail
        raw = await self._request("POST", "/v1/instant-analysis-feedback", json=body)
        return FeedbackResponse.model_validate(raw)
