"""OAuth response types."""

from __future__ import annotations

from pydantic import BaseModel


class OAuthTokenResponse(BaseModel):
    """OAuth2 access token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None

    model_config = {"extra": "allow"}
