"""Markdown report generator."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from llm_api_spec.models import Capability, CapabilityResult, ReportSummary, SchemaType


# Short human-readable descriptions for each capability check
_CAPABILITY_DESCRIPTIONS: dict[Capability, str] = {
    Capability.TEXT_INPUT: "Send a plain text prompt and verify the endpoint accepts it.",
    Capability.TEXT_OUTPUT: "Verify the response contains non-empty text content.",
    Capability.JSON_OUTPUT: "Request JSON output via response_format and validate it parses.",
    Capability.STRUCTURED_OUTPUT: "Enforce a JSON schema on the output and verify conformance.",
    Capability.TOOL_CALLING: "Provide a tool definition and verify the model emits a tool call.",
    Capability.TOOL_CHOICE_AUTO: "Set tool_choice='auto' and confirm the parameter is accepted.",
    Capability.TOOL_CHOICE_NONE: "Set tool_choice='none' and confirm tool calls are suppressed.",
    Capability.TOOL_CHOICE_REQUIRED: "Set tool_choice='required' and confirm a tool call is forced.",
    Capability.TOOL_CHOICE_FUNCTION: "Force a specific function via tool_choice and verify it is called.",
    Capability.MULTIPLE_TOOL_CALLS: "Prompt for multiple tool calls in a single response.",
    Capability.PARALLEL_TOOL_CALLS: "Set parallel_tool_calls=true and verify the parameter is accepted.",
    Capability.IMAGE_INPUT_URL: "Send an image via URL in the message content.",
    Capability.IMAGE_INPUT_BASE64: "Send a base64-encoded image in the message content.",
    Capability.IMAGE_INPUT_MULTI: "Send multiple images in a single message.",
    Capability.IMAGE_OUTPUT: "Request image generation and check for image content in response.",
    Capability.FILE_INPUT_INLINE: "Send an inline file attachment (Responses API only).",
    Capability.FILE_INPUT_REFERENCE: "Send a file reference by ID (Responses API only).",
    Capability.BUILT_IN_TOOLS: "Invoke a built-in tool like web search (Responses API only).",
    Capability.STREAMING: "Enable stream=true and verify chunked SSE delivery.",
    Capability.STOP_SEQUENCES: "Provide a stop sequence and verify the model halts at it.",
    Capability.LOGPROBS: "Request log probabilities and verify token-level data is returned.",
    Capability.SEEDED_DETERMINISM: "Send the same prompt twice with seed=42 and compare outputs.",
    Capability.LONG_PROMPT_ACCEPTANCE: "Send a ~22 KB prompt and verify the endpoint accepts it.",
    Capability.PREVIOUS_RESPONSE_ID: "Chain responses via previous_response_id (Responses API only).",
    Capability.BACKGROUND_MODE: "Request background execution mode (Responses API only).",
    Capability.RESPONSE_RETRIEVAL: "Retrieve a stored response by ID (Responses API only).",
    Capability.NORMALIZATION: "Verify the response can be normalized to the canonical format.",
    Capability.REGEX_CONSTRAINTS: "Apply a regex constraint on the output format.",
    Capability.GRAMMAR_CONSTRAINTS: "Apply a grammar constraint on the output format.",
    Capability.JSON_SCHEMA_CONSTRAINTS: "Apply a strict JSON schema constraint and verify compliance.",
}


# Keys to strip from raw responses for readability
_RESPONSE_STRIP_KEYS = {
    "content_filter_results",
    "prompt_filter_results",
    "usage",
    "system_fingerprint",
    "created",
    "service_tier",
    "object",
}

# Keys to strip from individual choice objects
_CHOICE_STRIP_KEYS = {
    "content_filter_results",
    "logprobs",
    "index",
}


def _clean_response(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    """Strip noise fields from a raw response for human-readable display."""
    if raw is None:
        return None
    cleaned = {}
    for k, v in raw.items():
        if k in _RESPONSE_STRIP_KEYS:
            continue
        if k == "choices" and isinstance(v, list):
            cleaned_choices = []
            for choice in v:
                if isinstance(choice, dict):
                    c = {ck: cv for ck, cv in choice.items() if ck not in _CHOICE_STRIP_KEYS}
                    # Clean message: drop annotations/refusal if empty
                    if "message" in c and isinstance(c["message"], dict):
                        msg = dict(c["message"])
                        if not msg.get("annotations"):
                            msg.pop("annotations", None)
                        if msg.get("refusal") is None:
                            msg.pop("refusal", None)
                        c["message"] = msg
                    cleaned_choices.append(c)
                else:
                    cleaned_choices.append(choice)
            cleaned["choices"] = cleaned_choices
        else:
            cleaned[k] = v
    return cleaned


def _clean_request(raw: dict[str, Any] | None) -> dict[str, Any] | None:
    """Strip noise fields from a raw request."""
    if raw is None:
        return None
    # Request is generally clean; just return as-is
    return raw


class MarkdownReporter:
    """Generates Markdown-formatted validation reports."""

    def generate(self, results: list[CapabilityResult]) -> str:
        """Generate summary-only markdown report."""
        return self._build_report(results, include_details=False)

    def generate_full(self, results: list[CapabilityResult]) -> str:
        """Generate full markdown report with summary + request/response details."""
        return self._build_report(results, include_details=True)

    def _build_report(self, results: list[CapabilityResult], include_details: bool) -> str:
        lines: list[str] = ["# LLM API Compatibility Report", ""]

        # Group by target
        targets: dict[str, list[CapabilityResult]] = {}
        for r in results:
            targets.setdefault(r.target, []).append(r)

        # ── SUMMARY SECTION ──
        lines.append("## Summary")
        lines.append("")
        for target_name, target_results in targets.items():
            summary = self._compute_summary(target_results)
            lines.append(f"**{target_name}** — "
                         f"{summary.passed} passed, "
                         f"{summary.failed} failed, "
                         f"{summary.unsupported} unsupported, "
                         f"{summary.not_applicable} n/a "
                         f"(out of {summary.total})")
            lines.append("")
        lines.append("---")
        lines.append("")

        # ── SIDE-BY-SIDE COMPARISON TABLE (multi-target only) ──
        if len(targets) > 1:
            lines.extend(self._build_comparison_table(targets))

        # ── RESULTS TABLE PER TARGET ──
        for target_name, target_results in targets.items():
            lines.append(f"## {target_name}")
            lines.append("")

            schemas: dict[SchemaType, list[CapabilityResult]] = {}
            for r in target_results:
                schemas.setdefault(r.schema_type, []).append(r)

            for schema_type, schema_results in schemas.items():
                lines.append(f"### {schema_type.value.replace('_', ' ').title()}")
                lines.append("")
                lines.append("| # | Capability | Result | Details |")
                lines.append("|---|-----------|--------|---------|")

                for i, r in enumerate(schema_results, 1):
                    status = r.status
                    icon = {"passed": "✅", "failed": "❌", "unsupported": "⚠️", "not_applicable": "➖"}.get(status, "?")
                    label = status.replace("_", " ")
                    details = (r.details or "")[:80]
                    cap_name = r.capability.value
                    if include_details:
                        anchor = f"{target_name}-{cap_name}".lower().replace(" ", "-").replace("_", "-")
                        cap_display = f"[{cap_name}](#{anchor})"
                    else:
                        cap_display = cap_name
                    lines.append(f"| {i} | {cap_display} | {icon} {label} | {details} |")

                lines.append("")

            lines.append("---")
            lines.append("")

        # ── DETAILS SECTION ──
        if include_details:
            lines.append("## Details")
            lines.append("")
            lines.append("Request/response payloads for each check (filtered for readability).")
            lines.append("")

            for target_name, target_results in targets.items():
                lines.append(f"### {target_name}")
                lines.append("")

                for r in target_results:
                    cap_name = r.capability.value
                    status = r.status
                    anchor_id = f"{target_name}-{cap_name}".lower().replace(" ", "-").replace("_", "-")

                    # Section heading with anchor
                    icon = {"passed": "✅", "failed": "❌", "unsupported": "⚠️", "not_applicable": "➖"}.get(status, "?")
                    lines.append(f'#### <a id="{anchor_id}"></a>{icon} {cap_name}')
                    lines.append("")

                    if r.details:
                        lines.append(f"> {r.details}")
                        lines.append("")

                    if r.errors:
                        lines.append("**Errors:**")
                        for err in r.errors:
                            lines.append(f"- {err}")
                        lines.append("")

                    if r.raw_request:
                        cleaned_req = _clean_request(r.raw_request)
                        lines.append("<details>")
                        lines.append("<summary>Request</summary>")
                        lines.append("")
                        lines.append("```json")
                        lines.append(json.dumps(cleaned_req, indent=2, default=str))
                        lines.append("```")
                        lines.append("</details>")
                        lines.append("")

                    if r.raw_response:
                        cleaned_resp = _clean_response(r.raw_response)
                        lines.append("<details>")
                        lines.append("<summary>Response</summary>")
                        lines.append("")
                        lines.append("```json")
                        lines.append(json.dumps(cleaned_resp, indent=2, default=str))
                        lines.append("```")
                        lines.append("</details>")
                        lines.append("")

                    lines.append("---")
                    lines.append("")

        return "\n".join(lines)

    def _icon(self, value: bool | None) -> str:
        if value is True:
            return "✓"
        elif value is False:
            return "✗"
        return "—"

    def _build_comparison_table(self, targets: dict[str, list[CapabilityResult]]) -> list[str]:
        """Build a side-by-side comparison table across all targets."""
        lines: list[str] = []
        lines.append("## Comparison")
        lines.append("")

        target_names = list(targets.keys())
        _STATUS_ICON = {"passed": "✅", "failed": "❌", "unsupported": "⚠️", "not_applicable": "➖"}

        # Group each target's results by (schema, capability) for lookup
        lookup: dict[str, dict[tuple[str, str], CapabilityResult]] = {}
        all_keys: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for name, results in targets.items():
            lookup[name] = {}
            for r in results:
                key = (r.schema_type.value, r.capability.value)
                lookup[name][key] = r
                if key not in seen:
                    all_keys.append(key)
                    seen.add(key)

        # Build table header
        header = "| # | Capability | " + " | ".join(target_names) + " |"
        separator = "|---|-----------|" + "|".join(":---:" for _ in target_names) + "|"
        lines.append(header)
        lines.append(separator)

        for i, (schema, cap) in enumerate(all_keys, 1):
            cells = []
            for name in target_names:
                r = lookup[name].get((schema, cap))
                if r:
                    status = r.status
                    icon = _STATUS_ICON.get(status, "?")
                    cells.append(icon)
                else:
                    cells.append("—")
            lines.append(f"| {i} | {cap} | " + " | ".join(cells) + " |")

        lines.append("")

        # Legend
        lines.append("✅ = passed · ❌ = failed · ⚠️ = unsupported · ➖ = n/a")
        lines.append("")
        lines.append("---")
        lines.append("")
        return lines

    def _compute_summary(self, results: list[CapabilityResult]) -> ReportSummary:
        summary = ReportSummary(total=len(results))
        for r in results:
            status = r.status
            if status == "passed":
                summary.passed += 1
            elif status == "failed":
                summary.failed += 1
            elif status == "unsupported":
                summary.unsupported += 1
            elif status == "not_applicable":
                summary.not_applicable += 1
        return summary
