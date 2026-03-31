"""Authentication response types."""

from __future__ import annotations

from pydantic import BaseModel


class AuthLoginResponse(BaseModel):
    """Response from the login endpoint."""

    id: int
    email: str
    name: str
    role: str
    org_slug: str
    token: str

    model_config = {"extra": "allow"}
