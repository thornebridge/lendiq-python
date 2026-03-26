"""OAuth resource — token endpoint using client credentials."""

from __future__ import annotations

from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource
from banklyze.types.oauth import OAuthTokenResponse


class OAuthResource(SyncAPIResource):

    def create_token(self, *, client_id: str, client_secret: str) -> OAuthTokenResponse:
        """Exchange client credentials for an access token.

        Uses HTTP Basic Auth (client_id:client_secret), not API key auth.
        """
        import base64

        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        data = self._request(
            "POST",
            "/v1/oauth/token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {creds}"},
        )
        return OAuthTokenResponse.model_validate(data)


class AsyncOAuthResource(AsyncAPIResource):

    async def create_token(self, *, client_id: str, client_secret: str) -> OAuthTokenResponse:
        """Exchange client credentials for an access token.

        Uses HTTP Basic Auth (client_id:client_secret), not API key auth.
        """
        import base64

        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        data = await self._request(
            "POST",
            "/v1/oauth/token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {creds}"},
        )
        return OAuthTokenResponse.model_validate(data)
