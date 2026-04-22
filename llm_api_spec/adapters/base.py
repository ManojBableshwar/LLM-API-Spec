"""Base schema adapter interface."""

from __future__ import annotations

import abc
import json
import sys
from typing import Any, AsyncIterator

import httpx

from llm_api_spec.models import EndpointTarget, NormalizedResponse, SchemaType


def _debug_log(label: str, data: Any) -> None:
    """Print debug info to stderr."""
    sep = "─" * 60
    print(f"\n{sep}", file=sys.stderr)
    print(f"DEBUG │ {label}", file=sys.stderr)
    print(sep, file=sys.stderr)
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str), file=sys.stderr)
    else:
        print(data, file=sys.stderr)
    print(sep, file=sys.stderr)


class SchemaAdapter(abc.ABC):
    """Base class for schema-specific adapters.

    Adapters know how to build requests, send them, parse responses,
    handle streaming, and normalize outputs for a specific schema.

    Adapters MUST NOT contain test logic, scoring logic, or assume backend behavior.
    """

    schema_type: SchemaType

    def __init__(self, target: EndpointTarget, *, debug: bool = False) -> None:
        self.target = target
        self.debug = debug
        self._client: httpx.AsyncClient | None = None

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            headers = dict(self.target.headers)
            if self.target.api_key:
                headers["Authorization"] = f"Bearer {self.target.api_key}"
            headers.setdefault("Content-Type", "application/json")
            self._client = httpx.AsyncClient(
                base_url=self.target.base_url,
                headers=headers,
                timeout=httpx.Timeout(self.target.timeout),
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @abc.abstractmethod
    def endpoint_path(self) -> str:
        """Return the API endpoint path (e.g., '/chat/completions')."""

    @abc.abstractmethod
    def build_request(self, **kwargs: Any) -> dict[str, Any]:
        """Build a request body from keyword arguments."""

    @abc.abstractmethod
    def parse_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        """Parse a raw response into a structured form."""

    @abc.abstractmethod
    def normalize(self, response_data: dict[str, Any]) -> NormalizedResponse:
        """Normalize a response into the canonical form."""

    @abc.abstractmethod
    async def stream_response(
        self, request_body: dict[str, Any]
    ) -> AsyncIterator[dict[str, Any]]:
        """Send a streaming request and yield parsed chunks."""

    async def send_request(self, request_body: dict[str, Any]) -> httpx.Response:
        """Send a non-streaming request and return the raw httpx response."""
        client = await self.get_client()
        url = self.endpoint_path()
        if self.debug:
            _debug_log(
                f"REQUEST → POST {self.target.base_url}{url}",
                request_body,
            )
        response = await client.post(url, json=request_body)
        if self.debug:
            _debug_log(
                f"RESPONSE ← {response.status_code}",
                {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text[:4000],
                },
            )
        return response

    async def send_and_parse(
        self, request_body: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Send request and return (raw_response_dict, parsed_response)."""
        response = await self.send_request(request_body)
        response.raise_for_status()
        raw = response.json()
        parsed = self.parse_response(raw)
        return raw, parsed

    async def retrieve_response(self, response_id: str) -> httpx.Response:
        """Retrieve a response by ID (for schemas that support it)."""
        if self.debug:
            _debug_log(f"RETRIEVE → GET /responses/{response_id}", {})
        raise NotImplementedError(
            f"{self.schema_type.value} does not support response retrieval"
        )
