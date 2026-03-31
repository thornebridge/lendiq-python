"""Collaboration resources — assignments, comments, doc requests, timeline, user search.

Contains sync and async classes for each sub-resource, plus standalone functions
for timeline and user search.
"""

from __future__ import annotations

from typing import Any

from lendiq._base_resource import AsyncAPIResource, SyncAPIResource
from lendiq.types.collaboration import (
    AssignedDealsResponse,
    Assignment,
    AssignmentListResponse,
    Comment,
    CommentListResponse,
    DocRequest,
    DocRequestListResponse,
    TimelineResponse,
    UserSearchResponse,
)
from lendiq.types.common import ActionResponse


# ── Comments ────────────────────────────────────────────────────────────────


class CommentsResource(SyncAPIResource):
    def list(self, deal_id: int) -> CommentListResponse:
        """List all comments on a deal."""
        data = self._request("GET", f"/v1/deals/{deal_id}/comments")
        return CommentListResponse.model_validate(data)

    def create(
        self,
        deal_id: int,
        *,
        content: str,
        parent_id: int | None = None,
    ) -> Comment:
        """Add a comment to a deal."""
        body: dict[str, Any] = {"content": content}
        if parent_id is not None:
            body["parent_id"] = parent_id
        data = self._request("POST", f"/v1/deals/{deal_id}/comments", json=body)
        return Comment.model_validate(data)

    def update(
        self,
        deal_id: int,
        comment_id: int,
        *,
        content: str,
    ) -> Comment:
        """Edit an existing comment."""
        data = self._request(
            "PATCH",
            f"/v1/deals/{deal_id}/comments/{comment_id}",
            json={"content": content},
        )
        return Comment.model_validate(data)

    def delete(self, deal_id: int, comment_id: int) -> ActionResponse:
        """Soft-delete a comment."""
        data = self._request("DELETE", f"/v1/deals/{deal_id}/comments/{comment_id}")
        return ActionResponse.model_validate(data)


class AsyncCommentsResource(AsyncAPIResource):
    async def list(self, deal_id: int) -> CommentListResponse:
        """List all comments on a deal."""
        data = await self._request("GET", f"/v1/deals/{deal_id}/comments")
        return CommentListResponse.model_validate(data)

    async def create(
        self,
        deal_id: int,
        *,
        content: str,
        parent_id: int | None = None,
    ) -> Comment:
        """Add a comment to a deal."""
        body: dict[str, Any] = {"content": content}
        if parent_id is not None:
            body["parent_id"] = parent_id
        data = await self._request("POST", f"/v1/deals/{deal_id}/comments", json=body)
        return Comment.model_validate(data)

    async def update(
        self,
        deal_id: int,
        comment_id: int,
        *,
        content: str,
    ) -> Comment:
        """Edit an existing comment."""
        data = await self._request(
            "PATCH",
            f"/v1/deals/{deal_id}/comments/{comment_id}",
            json={"content": content},
        )
        return Comment.model_validate(data)

    async def delete(self, deal_id: int, comment_id: int) -> ActionResponse:
        """Soft-delete a comment."""
        data = await self._request("DELETE", f"/v1/deals/{deal_id}/comments/{comment_id}")
        return ActionResponse.model_validate(data)


# ── Assignments ─────────────────────────────────────────────────────────────


class AssignmentsResource(SyncAPIResource):
    def list(self, deal_id: int) -> AssignmentListResponse:
        """List all assignments on a deal."""
        data = self._request("GET", f"/v1/deals/{deal_id}/assignments")
        return AssignmentListResponse.model_validate(data)

    def create(
        self,
        deal_id: int,
        *,
        user_id: int,
        role: str = "assignee",
    ) -> Assignment:
        """Assign a user to a deal."""
        data = self._request(
            "POST",
            f"/v1/deals/{deal_id}/assignments",
            json={"user_id": user_id, "role": role},
        )
        return Assignment.model_validate(data)

    def delete(self, deal_id: int, user_id: int) -> ActionResponse:
        """Remove a user's assignment from a deal."""
        data = self._request("DELETE", f"/v1/deals/{deal_id}/assignments/{user_id}")
        return ActionResponse.model_validate(data)

    def my_deals(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
    ) -> AssignedDealsResponse:
        """List deals assigned to the current user."""
        data = self._request(
            "GET",
            "/v1/me/assigned-deals",
            params={"page": page, "per_page": per_page},
        )
        return AssignedDealsResponse.model_validate(data)


class AsyncAssignmentsResource(AsyncAPIResource):
    async def list(self, deal_id: int) -> AssignmentListResponse:
        """List all assignments on a deal."""
        data = await self._request("GET", f"/v1/deals/{deal_id}/assignments")
        return AssignmentListResponse.model_validate(data)

    async def create(
        self,
        deal_id: int,
        *,
        user_id: int,
        role: str = "assignee",
    ) -> Assignment:
        """Assign a user to a deal."""
        data = await self._request(
            "POST",
            f"/v1/deals/{deal_id}/assignments",
            json={"user_id": user_id, "role": role},
        )
        return Assignment.model_validate(data)

    async def delete(self, deal_id: int, user_id: int) -> ActionResponse:
        """Remove a user's assignment from a deal."""
        data = await self._request("DELETE", f"/v1/deals/{deal_id}/assignments/{user_id}")
        return ActionResponse.model_validate(data)

    async def my_deals(
        self,
        *,
        page: int = 1,
        per_page: int = 25,
    ) -> AssignedDealsResponse:
        """List deals assigned to the current user."""
        data = await self._request(
            "GET",
            "/v1/me/assigned-deals",
            params={"page": page, "per_page": per_page},
        )
        return AssignedDealsResponse.model_validate(data)


# ── Document Requests ───────────────────────────────────────────────────────


class DocRequestsResource(SyncAPIResource):
    def list(self, deal_id: int) -> DocRequestListResponse:
        """List all document requests on a deal."""
        data = self._request("GET", f"/v1/deals/{deal_id}/doc-requests")
        return DocRequestListResponse.model_validate(data)

    def create(
        self,
        deal_id: int,
        *,
        document_type: str,
        description: str | None = None,
        recipient_email: str | None = None,
        due_date: str | None = None,
    ) -> DocRequest:
        """Create a new document request on a deal."""
        body: dict[str, Any] = {"document_type": document_type}
        if description is not None:
            body["description"] = description
        if recipient_email is not None:
            body["recipient_email"] = recipient_email
        if due_date is not None:
            body["due_date"] = due_date
        data = self._request("POST", f"/v1/deals/{deal_id}/doc-requests", json=body)
        return DocRequest.model_validate(data)

    def update(
        self,
        deal_id: int,
        doc_request_id: int,
        *,
        status: str,
        document_id: int | None = None,
    ) -> DocRequest:
        """Update a document request status (received or cancelled)."""
        body: dict[str, Any] = {"status": status}
        if document_id is not None:
            body["document_id"] = document_id
        data = self._request(
            "PATCH",
            f"/v1/deals/{deal_id}/doc-requests/{doc_request_id}",
            json=body,
        )
        return DocRequest.model_validate(data)


class AsyncDocRequestsResource(AsyncAPIResource):
    async def list(self, deal_id: int) -> DocRequestListResponse:
        """List all document requests on a deal."""
        data = await self._request("GET", f"/v1/deals/{deal_id}/doc-requests")
        return DocRequestListResponse.model_validate(data)

    async def create(
        self,
        deal_id: int,
        *,
        document_type: str,
        description: str | None = None,
        recipient_email: str | None = None,
        due_date: str | None = None,
    ) -> DocRequest:
        """Create a new document request on a deal."""
        body: dict[str, Any] = {"document_type": document_type}
        if description is not None:
            body["description"] = description
        if recipient_email is not None:
            body["recipient_email"] = recipient_email
        if due_date is not None:
            body["due_date"] = due_date
        data = await self._request("POST", f"/v1/deals/{deal_id}/doc-requests", json=body)
        return DocRequest.model_validate(data)

    async def update(
        self,
        deal_id: int,
        doc_request_id: int,
        *,
        status: str,
        document_id: int | None = None,
    ) -> DocRequest:
        """Update a document request status (received or cancelled)."""
        body: dict[str, Any] = {"status": status}
        if document_id is not None:
            body["document_id"] = document_id
        data = await self._request(
            "PATCH",
            f"/v1/deals/{deal_id}/doc-requests/{doc_request_id}",
            json=body,
        )
        return DocRequest.model_validate(data)


# ── Timeline ───────────────────────────────────────────────────────────────


class TimelineResource(SyncAPIResource):
    def deal_timeline(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> TimelineResponse:
        """Get the activity timeline for a deal."""
        data = self._request(
            "GET",
            f"/v1/deals/{deal_id}/timeline",
            params={"page": page, "per_page": per_page},
        )
        return TimelineResponse.model_validate(data)

    def org_activity(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> TimelineResponse:
        """Get the organization-wide activity feed."""
        data = self._request(
            "GET",
            "/v1/activity",
            params={"page": page, "per_page": per_page},
        )
        return TimelineResponse.model_validate(data)


class AsyncTimelineResource(AsyncAPIResource):
    async def deal_timeline(
        self,
        deal_id: int,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> TimelineResponse:
        """Get the activity timeline for a deal."""
        data = await self._request(
            "GET",
            f"/v1/deals/{deal_id}/timeline",
            params={"page": page, "per_page": per_page},
        )
        return TimelineResponse.model_validate(data)

    async def org_activity(
        self,
        *,
        page: int = 1,
        per_page: int = 50,
    ) -> TimelineResponse:
        """Get the organization-wide activity feed."""
        data = await self._request(
            "GET",
            "/v1/activity",
            params={"page": page, "per_page": per_page},
        )
        return TimelineResponse.model_validate(data)


# ── User Search ─────────────────────────────────────────────────────────────


class UserSearchResource(SyncAPIResource):
    def search(self, q: str) -> UserSearchResponse:
        """Search for users in the organization by name or email."""
        data = self._request("GET", "/v1/users/search", params={"q": q})
        return UserSearchResponse.model_validate(data)


class AsyncUserSearchResource(AsyncAPIResource):
    async def search(self, q: str) -> UserSearchResponse:
        """Search for users in the organization by name or email."""
        data = await self._request("GET", "/v1/users/search", params={"q": q})
        return UserSearchResponse.model_validate(data)
