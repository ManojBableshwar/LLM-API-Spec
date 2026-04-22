"""Unit tests for reporting system."""

from __future__ import annotations

import json

import pytest

from llm_api_spec.models import Capability, CapabilityResult, SchemaType
from llm_api_spec.reporting.json_report import JSONReporter
from llm_api_spec.reporting.markdown_report import MarkdownReporter


def _make_result(
    cap: Capability,
    supported: bool | None = True,
    passed: bool | None = True,
    target: str = "test",
    schema: SchemaType = SchemaType.CHAT_COMPLETIONS,
) -> CapabilityResult:
    return CapabilityResult(
        target=target,
        schema=schema,
        capability=cap,
        supported=supported,
        details=f"Test {cap.value}",
        **{"pass": passed},
    )


class TestJSONReporter:
    def test_empty_results(self):
        reporter = JSONReporter()
        output = reporter.generate([])
        data = json.loads(output)
        assert data["results"] == []
        assert data["summary"]["total"] == 0

    def test_single_passed(self):
        results = [_make_result(Capability.TEXT_INPUT)]
        reporter = JSONReporter()
        output = reporter.generate(results)
        data = json.loads(output)
        assert len(data["results"]) == 1
        assert data["results"][0]["capability"] == "text_input"
        assert data["results"][0]["supported"] is True
        assert data["results"][0]["pass"] is True
        assert data["summary"]["passed"] == 1

    def test_mixed_results(self):
        results = [
            _make_result(Capability.TEXT_INPUT, supported=True, passed=True),
            _make_result(Capability.TEXT_OUTPUT, supported=True, passed=False),
            _make_result(Capability.TOOL_CALLING, supported=False, passed=None),
            _make_result(Capability.LOGPROBS, supported=None, passed=None),
        ]
        reporter = JSONReporter()
        output = reporter.generate(results)
        data = json.loads(output)
        assert data["summary"]["passed"] == 1
        assert data["summary"]["failed"] == 1
        assert data["summary"]["unsupported"] == 1
        assert data["summary"]["not_applicable"] == 1

    def test_full_report(self):
        results = [
            CapabilityResult(
                target="test",
                schema=SchemaType.CHAT_COMPLETIONS,
                capability=Capability.TEXT_INPUT,
                supported=True,
                raw_request={"model": "m"},
                raw_response={"id": "1"},
                **{"pass": True},
            )
        ]
        reporter = JSONReporter()
        output = reporter.generate_full(results)
        data = json.loads(output)
        assert data["results"][0]["raw_request"] == {"model": "m"}


class TestMarkdownReporter:
    def test_empty_results(self):
        reporter = MarkdownReporter()
        output = reporter.generate([])
        assert "# LLM API Compatibility Report" in output

    def test_single_result(self):
        results = [_make_result(Capability.TEXT_INPUT)]
        reporter = MarkdownReporter()
        output = reporter.generate(results)
        assert "text_input" in output
        assert "✅" in output
        assert "1 passed" in output

    def test_failed_result(self):
        results = [_make_result(Capability.TEXT_INPUT, supported=True, passed=False)]
        reporter = MarkdownReporter()
        output = reporter.generate(results)
        assert "❌" in output
        assert "1 failed" in output

    def test_multiple_targets(self):
        results = [
            _make_result(Capability.TEXT_INPUT, target="target-a"),
            _make_result(Capability.TEXT_INPUT, target="target-b"),
        ]
        reporter = MarkdownReporter()
        output = reporter.generate(results)
        assert "target-a" in output
        assert "target-b" in output

    def test_multiple_schemas(self):
        results = [
            _make_result(
                Capability.TEXT_INPUT,
                schema=SchemaType.CHAT_COMPLETIONS,
            ),
            _make_result(
                Capability.TEXT_INPUT,
                schema=SchemaType.RESPONSES,
            ),
        ]
        reporter = MarkdownReporter()
        output = reporter.generate(results)
        assert "Chat Completions" in output
        assert "Responses" in output

    def test_icon_values(self):
        reporter = MarkdownReporter()
        assert reporter._icon(True) == "✓"
        assert reporter._icon(False) == "✗"
        assert reporter._icon(None) == "—"
