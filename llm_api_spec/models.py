"""Data models for llm-api-spec."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SchemaType(str, Enum):
    CHAT_COMPLETIONS = "chat_completions"
    RESPONSES = "responses"


class Capability(str, Enum):
    TEXT_INPUT = "text_input"
    TEXT_OUTPUT = "text_output"
    JSON_OUTPUT = "json_output"
    STRUCTURED_OUTPUT = "structured_output"
    TOOL_CALLING = "tool_calling"
    TOOL_CHOICE_AUTO = "tool_choice_auto"
    TOOL_CHOICE_NONE = "tool_choice_none"
    TOOL_CHOICE_REQUIRED = "tool_choice_required"
    TOOL_CHOICE_FUNCTION = "tool_choice_function"
    MULTIPLE_TOOL_CALLS = "multiple_tool_calls"
    PARALLEL_TOOL_CALLS = "parallel_tool_calls"
    IMAGE_INPUT_URL = "image_input_url"
    IMAGE_INPUT_BASE64 = "image_input_base64"
    IMAGE_INPUT_MULTI = "image_input_multi"
    IMAGE_OUTPUT = "image_output"
    FILE_INPUT_INLINE = "file_input_inline"
    FILE_INPUT_REFERENCE = "file_input_reference"
    BUILT_IN_TOOLS = "built_in_tools"
    STREAMING = "streaming"
    STOP_SEQUENCES = "stop_sequences"
    LOGPROBS = "logprobs"
    SEEDED_DETERMINISM = "seeded_determinism"
    LONG_PROMPT_ACCEPTANCE = "long_prompt_acceptance"
    PREVIOUS_RESPONSE_ID = "previous_response_id"
    BACKGROUND_MODE = "background_mode"
    RESPONSE_RETRIEVAL = "response_retrieval"
    NORMALIZATION = "normalization"
    REGEX_CONSTRAINTS = "regex_constraints"
    GRAMMAR_CONSTRAINTS = "grammar_constraints"
    JSON_SCHEMA_CONSTRAINTS = "json_schema_constraints"


# Capabilities that only apply to specific schemas
CHAT_COMPLETIONS_ONLY: set[Capability] = {
    Capability.LOGPROBS,
}

RESPONSES_ONLY: set[Capability] = {
    Capability.FILE_INPUT_INLINE,
    Capability.FILE_INPUT_REFERENCE,
    Capability.BUILT_IN_TOOLS,
    Capability.PREVIOUS_RESPONSE_ID,
    Capability.BACKGROUND_MODE,
    Capability.RESPONSE_RETRIEVAL,
}


def is_applicable(capability: Capability, schema: SchemaType) -> bool:
    """Check if a capability is applicable to a given schema."""
    if schema == SchemaType.CHAT_COMPLETIONS and capability in RESPONSES_ONLY:
        return False
    if schema == SchemaType.RESPONSES and capability in CHAT_COMPLETIONS_ONLY:
        return False
    return True


class EndpointTarget(BaseModel):
    """A concrete HTTP endpoint to be verified."""

    name: str
    base_url: str
    api_key: str | None = None
    model: str
    schemas: list[SchemaType] = Field(default_factory=lambda: [SchemaType.CHAT_COMPLETIONS])
    headers: dict[str, str] = Field(default_factory=dict)
    timeout: float = 60.0


class CapabilityResult(BaseModel):
    """Result of a single capability check."""

    target: str
    schema_type: SchemaType = Field(alias="schema")
    capability: Capability
    supported: bool | None = None
    passed: bool | None = Field(None, alias="pass")
    request_schema_valid: bool | None = None
    response_schema_valid: bool | None = None
    normalized: bool | None = None
    details: str | None = None
    raw_request: dict[str, Any] | None = None
    raw_response: dict[str, Any] | None = None
    normalized_response: dict[str, Any] | None = None
    errors: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}

    @property
    def status(self) -> str:
        if self.supported is None:
            return "not_applicable"
        if not self.supported:
            return "unsupported"
        if self.passed:
            return "passed"
        return "failed"


class NormalizedResponse(BaseModel):
    """Canonical internal representation of a response."""

    text: str | None = None
    tool_calls: list[NormalizedToolCall] = Field(default_factory=list)
    finish_reason: str | None = None
    model: str | None = None
    usage: NormalizedUsage | None = None
    response_id: str | None = None


class NormalizedToolCall(BaseModel):
    """Canonical tool call representation."""

    id: str | None = None
    name: str
    arguments: str


class NormalizedUsage(BaseModel):
    """Canonical usage representation."""

    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class ValidationReport(BaseModel):
    """Aggregate report over all results."""

    results: list[CapabilityResult] = Field(default_factory=list)
    summary: ReportSummary | None = None


class ReportSummary(BaseModel):
    """Summary counts for a report."""

    total: int = 0
    passed: int = 0
    failed: int = 0
    unsupported: int = 0
    not_applicable: int = 0
