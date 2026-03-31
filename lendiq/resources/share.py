"""Share resource — create, list, and revoke deal share links.

Contains both synchronous (SharesResource) and asynchronous (AsyncSharesResource)
implementations. All methods return typed Pydantic models.
"""

from __future__ import annotations

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.share import ShareToken, ShareTokenListResponse


# ── Sync resource ────────────────────────────────────────────────────────────


class SharesResource(SyncAPIResource):

    def create(
        self,
        deal_id: int,
        *,
        view_mode: str = "summary",
        expires_in_days: int = 7,
    ) -> ShareToken:
        """Create a shareable link for a deal.

        Args:
            deal_id: The deal to share.
            view_mode: ``"summary"`` or ``"full"`` (default ``"summary"``).
            expires_in_days: Link expiry in days (1-365, default 7).
        """
        body = {"view_mode": view_mode, "expires_in_days": expires_in_days}
        data = self._request("POST", f"/v1/deals/{deal_id}/share", json=body)
        return ShareToken.model_validate(data)

    def list(self, deal_id: int) -> ShareTokenListResponse:
        """List active share tokens for a deal.

        Args:
            deal_id: The deal whose share links to list.
        """
        data = self._request("GET", f"/v1/deals/{deal_id}/shares")
        return ShareTokenListResponse.model_validate(data)

    def revoke(self, deal_id: int, share_id: int) -> None:
        """Revoke a share token.

        Args:
            deal_id: The deal the share token belongs to.
            share_id: The ID of the share token to revoke.
        """
        self._request("DELETE", f"/v1/deals/{deal_id}/shares/{share_id}")


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncSharesResource(AsyncAPIResource):

    async def create(
        self,
        deal_id: int,
        *,
        view_mode: str = "summary",
        expires_in_days: int = 7,
    ) -> ShareToken:
        """Create a shareable link for a deal.

        Args:
            deal_id: The deal to share.
            view_mode: ``"summary"`` or ``"full"`` (default ``"summary"``).
            expires_in_days: Link expiry in days (1-365, default 7).
        """
        body = {"view_mode": view_mode, "expires_in_days": expires_in_days}
        data = await self._request("POST", f"/v1/deals/{deal_id}/share", json=body)
        return ShareToken.model_validate(data)

    async def list(self, deal_id: int) -> ShareTokenListResponse:
        """List active share tokens for a deal.

        Args:
            deal_id: The deal whose share links to list.
        """
        data = await self._request("GET", f"/v1/deals/{deal_id}/shares")
        return ShareTokenListResponse.model_validate(data)

    async def revoke(self, deal_id: int, share_id: int) -> None:
        """Revoke a share token.

        Args:
            deal_id: The deal the share token belongs to.
            share_id: The ID of the share token to revoke.
        """
        await self._request("DELETE", f"/v1/deals/{deal_id}/shares/{share_id}")
