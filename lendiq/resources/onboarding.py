"""Onboarding resource — demo data seeding for first-run experience.

Contains both synchronous (OnboardingResource) and asynchronous
(AsyncOnboardingResource) implementations.
"""

from __future__ import annotations

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.common import ActionResponse


# ── Sync resource ────────────────────────────────────────────────────────────


class OnboardingResource(SyncAPIResource):

    def seed_demo(self) -> ActionResponse:
        """Seed demo deals and documents for the first-run experience.

        Idempotent: only runs once per organization (checks the org's
        ``demo_seeded`` flag).
        """
        data = self._request("POST", "/v1/onboarding/seed-demo")
        return ActionResponse.model_validate(data)


# ── Async resource ───────────────────────────────────────────────────────────


class AsyncOnboardingResource(AsyncAPIResource):

    async def seed_demo(self) -> ActionResponse:
        """Seed demo deals and documents for the first-run experience.

        Idempotent: only runs once per organization (checks the org's
        ``demo_seeded`` flag).
        """
        data = await self._request("POST", "/v1/onboarding/seed-demo")
        return ActionResponse.model_validate(data)
