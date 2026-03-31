"""Keys resource — create, list, and revoke API keys.

Contains both synchronous (KeysResource) and asynchronous (AsyncKeysResource)
implementations. All methods return typed Pydantic models.
"""

from __future__ import annotations

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse
from lendiq.types.key import CreateKeyResponse, KeyListResponse


# ── Sync resource ────────────────────────────────────────────────────────────


class KeysResource(SyncAPIResource):
    def create(
        self,
        *,
        name: str,
        scopes: str = "read,write",
        expires_in_days: int | None = None,
    ) -> CreateKeyResponse:
        """Create a new API key.

        The raw key is returned ONLY in this response. Store it securely.

        Args:
            name: A descriptive name for the key.
            scopes: Comma-separated scopes (default ``"read,write"``).
            expires_in_days: Optional expiry in days (1-365).
        """
        body: dict = {"name": name, "scopes": scopes}
        if expires_in_days is not None:
            body["expires_in_days"] = expires_in_days
        data = self._request("POST", "/v1/keys", json=body)
        return CreateKeyResponse.model_validate(data)

    def list(self) -> KeyListResponse:
        """List all API keys for the authenticated organization."""
        data = self._request("GET", "/v1/keys")
        return KeyListResponse.model_validate(data)

    def revoke(self, key_id: int) -> ActionResponse:
        """Revoke an API key. The key will immediately stop working.

        Args:
            key_id: The ID of the API key to revoke.
        """
        data = self._request("DELETE", f"/v1/keys/{key_id}")
        return ActionResponse.model_validate(data)


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncKeysResource(AsyncAPIResource):
    async def create(
        self,
        *,
        name: str,
        scopes: str = "read,write",
        expires_in_days: int | None = None,
    ) -> CreateKeyResponse:
        """Create a new API key.

        The raw key is returned ONLY in this response. Store it securely.

        Args:
            name: A descriptive name for the key.
            scopes: Comma-separated scopes (default ``"read,write"``).
            expires_in_days: Optional expiry in days (1-365).
        """
        body: dict = {"name": name, "scopes": scopes}
        if expires_in_days is not None:
            body["expires_in_days"] = expires_in_days
        data = await self._request("POST", "/v1/keys", json=body)
        return CreateKeyResponse.model_validate(data)

    async def list(self) -> KeyListResponse:
        """List all API keys for the authenticated organization."""
        data = await self._request("GET", "/v1/keys")
        return KeyListResponse.model_validate(data)

    async def revoke(self, key_id: int) -> ActionResponse:
        """Revoke an API key. The key will immediately stop working.

        Args:
            key_id: The ID of the API key to revoke.
        """
        data = await self._request("DELETE", f"/v1/keys/{key_id}")
        return ActionResponse.model_validate(data)
