"""JSON report generator."""

from __future__ import annotations

import json
from typing import Any

from llm_api_spec.models import CapabilityResult, ReportSummary, ValidationReport


class JSONReporter:
    """Generates JSON-formatted validation reports."""

    def generate(self, results: list[CapabilityResult]) -> str:
        summary = self._compute_summary(results)
        report = ValidationReport(results=results, summary=summary)

        output: dict[str, Any] = {
            "results": [],
            "summary": summary.model_dump(),
        }

        for r in results:
            output["results"].append({
                "target": r.target,
                "schema": r.schema_type.value,
                "capability": r.capability.value,
                "supported": r.supported,
                "pass": r.passed,
                "request_schema_valid": r.request_schema_valid,
                "response_schema_valid": r.response_schema_valid,
                "normalized": r.normalized,
                "details": r.details,
                "errors": r.errors,
            })

        return json.dumps(output, indent=2)

    def generate_full(self, results: list[CapabilityResult]) -> str:
        """Generate full report including raw request/response data."""
        summary = self._compute_summary(results)

        output: dict[str, Any] = {
            "results": [],
            "summary": summary.model_dump(),
        }

        for r in results:
            output["results"].append({
                "target": r.target,
                "schema": r.schema_type.value,
                "capability": r.capability.value,
                "supported": r.supported,
                "pass": r.passed,
                "request_schema_valid": r.request_schema_valid,
                "response_schema_valid": r.response_schema_valid,
                "normalized": r.normalized,
                "details": r.details,
                "raw_request": r.raw_request,
                "raw_response": r.raw_response,
                "normalized_response": r.normalized_response,
                "errors": r.errors,
            })

        return json.dumps(output, indent=2)

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
