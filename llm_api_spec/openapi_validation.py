"""OpenAPI request/response validation layer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from llm_api_spec.models import SchemaType


class OpenAPIValidator:
    """Validates requests and responses against OpenAPI specifications."""

    def __init__(self, schema_type: SchemaType, spec_path: str | Path | None = None):
        self.schema_type = schema_type
        self._spec: dict[str, Any] | None = None
        self._spec_path = spec_path

        if spec_path:
            self._load_spec(Path(spec_path))

    def _load_spec(self, path: Path) -> None:
        if path.exists():
            with open(path) as f:
                if path.suffix in (".yaml", ".yml"):
                    import yaml

                    self._spec = yaml.safe_load(f)
                else:
                    self._spec = json.load(f)

    @property
    def is_loaded(self) -> bool:
        return self._spec is not None

    def validate_request(self, request_body: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate a request body against the OpenAPI spec.

        Returns (is_valid, errors).
        """
        if not self._spec:
            return True, []

        errors: list[str] = []

        try:
            endpoint = self._get_endpoint_schema("request")
            if endpoint:
                self._validate_against_schema(request_body, endpoint, errors, "request")
        except Exception as exc:
            errors.append(f"Validation error: {exc}")

        return len(errors) == 0, errors

    def validate_response(self, response_body: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate a response body against the OpenAPI spec.

        Returns (is_valid, errors).
        """
        if not self._spec:
            return True, []

        errors: list[str] = []

        try:
            endpoint = self._get_endpoint_schema("response")
            if endpoint:
                self._validate_against_schema(response_body, endpoint, errors, "response")
        except Exception as exc:
            errors.append(f"Validation error: {exc}")

        return len(errors) == 0, errors

    def _get_endpoint_schema(self, direction: str) -> dict[str, Any] | None:
        """Extract the relevant schema from the OpenAPI spec."""
        if not self._spec:
            return None

        paths = self._spec.get("paths", {})

        if self.schema_type == SchemaType.CHAT_COMPLETIONS:
            path_key = "/chat/completions"
        else:
            path_key = "/responses"

        path_spec = paths.get(path_key, {})
        post_spec = path_spec.get("post", {})

        if direction == "request":
            request_body = post_spec.get("requestBody", {})
            content = request_body.get("content", {})
            json_content = content.get("application/json", {})
            return json_content.get("schema")
        else:
            responses = post_spec.get("responses", {})
            success = responses.get("200", responses.get("201", {}))
            content = success.get("content", {})
            json_content = content.get("application/json", {})
            return json_content.get("schema")

    def _validate_against_schema(
        self,
        data: dict[str, Any],
        schema: dict[str, Any],
        errors: list[str],
        context: str,
    ) -> None:
        """Validate data against a JSON schema, collecting errors."""
        try:
            import jsonschema

            # Resolve $ref references if possible
            resolved_schema = self._resolve_refs(schema)
            jsonschema.validate(instance=data, schema=resolved_schema)
        except ImportError:
            errors.append("jsonschema package not available for validation")
        except Exception as exc:
            errors.append(f"{context} validation: {exc}")

    def _resolve_refs(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Attempt to resolve $ref references in the schema."""
        if not self._spec:
            return schema

        if isinstance(schema, dict):
            if "$ref" in schema:
                ref_path = schema["$ref"]
                if ref_path.startswith("#/"):
                    parts = ref_path[2:].split("/")
                    resolved = self._spec
                    for part in parts:
                        resolved = resolved.get(part, {})
                    return self._resolve_refs(resolved) if isinstance(resolved, dict) else resolved
                return schema
            return {k: self._resolve_refs(v) for k, v in schema.items()}
        elif isinstance(schema, list):
            return [self._resolve_refs(item) for item in schema]
        return schema
