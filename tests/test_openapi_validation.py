"""Unit tests for OpenAPI validation layer."""

from __future__ import annotations

import pytest

from llm_api_spec.models import SchemaType
from llm_api_spec.openapi_validation import OpenAPIValidator


class TestOpenAPIValidator:
    def test_no_spec_loaded(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        assert not v.is_loaded
        valid, errors = v.validate_request({"model": "m", "messages": []})
        assert valid
        assert errors == []

    def test_validate_request_no_spec(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        valid, errors = v.validate_request({"model": "m"})
        assert valid

    def test_validate_response_no_spec(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        valid, errors = v.validate_response({"id": "1"})
        assert valid

    def test_nonexistent_spec_path(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS, spec_path="/nonexistent.json")
        assert not v.is_loaded

    def test_resolve_refs_no_spec(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        schema = {"type": "object", "properties": {"x": {"type": "string"}}}
        resolved = v._resolve_refs(schema)
        assert resolved == schema

    def test_resolve_refs_with_ref(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        v._spec = {
            "components": {
                "schemas": {
                    "Message": {"type": "object", "properties": {"role": {"type": "string"}}}
                }
            }
        }
        schema = {"$ref": "#/components/schemas/Message"}
        resolved = v._resolve_refs(schema)
        assert resolved["type"] == "object"

    def test_resolve_refs_nested(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        v._spec = {
            "components": {
                "schemas": {
                    "Inner": {"type": "string"}
                }
            }
        }
        schema = {
            "type": "object",
            "properties": {
                "field": {"$ref": "#/components/schemas/Inner"}
            },
        }
        resolved = v._resolve_refs(schema)
        assert resolved["properties"]["field"] == {"type": "string"}

    def test_get_endpoint_schema_chat(self):
        v = OpenAPIValidator(SchemaType.CHAT_COMPLETIONS)
        v._spec = {
            "paths": {
                "/chat/completions": {
                    "post": {
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "object"}
                                    }
                                }
                            }
                        },
                    }
                }
            }
        }
        req_schema = v._get_endpoint_schema("request")
        assert req_schema == {"type": "object"}
        resp_schema = v._get_endpoint_schema("response")
        assert resp_schema == {"type": "object"}

    def test_get_endpoint_schema_responses(self):
        v = OpenAPIValidator(SchemaType.RESPONSES)
        v._spec = {"paths": {"/responses": {"post": {"requestBody": {"content": {}}}}}}
        req_schema = v._get_endpoint_schema("request")
        assert req_schema is None
