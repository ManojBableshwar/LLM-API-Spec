"""CLI entry point for llm-api-validate."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

import click
import yaml

from llm_api_spec.models import Capability, EndpointTarget, SchemaType
from llm_api_spec.reporting.json_report import JSONReporter
from llm_api_spec.reporting.markdown_report import MarkdownReporter
from llm_api_spec.runner import run_all_checks


def _resolve_env_vars(value: str) -> str:
    """Resolve ${VAR_NAME} patterns in strings."""
    if not isinstance(value, str):
        return value
    import re

    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        return os.environ.get(var_name, match.group(0))

    return re.sub(r"\$\{(\w+)\}", replacer, value)


def _load_config(config_path: str) -> list[EndpointTarget]:
    """Load targets from a YAML config file."""
    path = Path(config_path)
    if not path.exists():
        raise click.ClickException(f"Config file not found: {config_path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    targets: list[EndpointTarget] = []
    for t in data.get("targets", []):
        # Resolve env vars in string fields
        for key in ("base_url", "api_key", "model", "name"):
            if key in t and isinstance(t[key], str):
                t[key] = _resolve_env_vars(t[key])

        # Resolve env vars in headers
        if "headers" in t:
            t["headers"] = {k: _resolve_env_vars(v) for k, v in t["headers"].items()}

        # Convert schema strings to enum values
        if "schemas" in t:
            t["schemas"] = [SchemaType(s) for s in t["schemas"]]

        targets.append(EndpointTarget(**t))

    return targets


def _parse_capabilities(capabilities_str: str) -> list[Capability] | None:
    """Parse a comma-separated list of capability names."""
    if capabilities_str == "all":
        return None
    caps = []
    for name in capabilities_str.split(","):
        name = name.strip()
        try:
            caps.append(Capability(name))
        except ValueError:
            raise click.ClickException(f"Unknown capability: {name}")
    return caps


@click.command("llm-api-validate")
@click.option("--config", "config_path", type=str, default=None, help="Path to YAML config file")
@click.option("--target", "target_url", type=str, default=None, help="Inline target URL")
@click.option("--model", "model_name", type=str, default=None, help="Model identifier")
@click.option("--api-key", "api_key", type=str, default=None, help="API key")
@click.option(
    "--schema",
    "schema_filter",
    type=click.Choice(["chat_completions", "responses", "all"]),
    default="all",
    help="Schema(s) to test",
)
@click.option("--capabilities", type=str, default="all", help="Comma-separated capabilities or 'all'")
@click.option(
    "--output",
    "output_format",
    type=click.Choice(["json", "markdown"]),
    default="markdown",
    help="Output format",
)
@click.option("--output-file", type=str, default=None, help="Write output to file")
@click.option("--openapi-validation/--no-openapi-validation", default=False, help="Enable OpenAPI validation")
@click.option("--timeout", type=float, default=60.0, help="Request timeout in seconds")
@click.option("--verbose/--no-verbose", default=False, help="Verbose output")
@click.option("--debug/--no-debug", default=False, help="Log every HTTP request and response to stderr")
def main(
    config_path: str | None,
    target_url: str | None,
    model_name: str | None,
    api_key: str | None,
    schema_filter: str,
    capabilities: str,
    output_format: str,
    output_file: str | None,
    openapi_validation: bool,
    timeout: float,
    verbose: bool,
    debug: bool,
) -> None:
    """Validate LLM API endpoint compatibility."""
    # Build targets list
    targets: list[EndpointTarget] = []

    if config_path:
        targets = _load_config(config_path)
        # Filter by target name if specified
        if target_url:
            targets = [t for t in targets if t.name == target_url]
            if not targets:
                raise click.ClickException(f"Target '{target_url}' not found in config")
    elif target_url:
        if not model_name:
            raise click.ClickException("--model is required when using --target")

        schemas: list[SchemaType] = []
        if schema_filter == "all":
            schemas = [SchemaType.CHAT_COMPLETIONS, SchemaType.RESPONSES]
        else:
            schemas = [SchemaType(schema_filter)]

        targets.append(
            EndpointTarget(
                name="inline-target",
                base_url=target_url,
                api_key=api_key,
                model=model_name,
                schemas=schemas,
                timeout=timeout,
            )
        )
    else:
        raise click.ClickException("Either --config or --target is required")

    # Apply schema filter to config-loaded targets
    if config_path and schema_filter != "all":
        filter_schema = SchemaType(schema_filter)
        for t in targets:
            t.schemas = [s for s in t.schemas if s == filter_schema]

    # Parse capabilities
    caps = _parse_capabilities(capabilities)

    # Run checks
    try:
        results = asyncio.run(
            run_all_checks(
                targets=targets,
                capabilities=caps,
                openapi_validation=openapi_validation,
                verbose=verbose or debug,
                debug=debug,
            )
        )
    except Exception as exc:
        raise click.ClickException(f"Validation failed: {exc}")

    # Generate report
    if output_format == "json":
        reporter = JSONReporter()
        report = reporter.generate_full(results) if debug else reporter.generate(results)
    else:
        reporter = MarkdownReporter()
        report = reporter.generate_full(results) if debug else reporter.generate(results)

    # Output
    if output_file:
        Path(output_file).write_text(report)
        if verbose:
            click.echo(f"Report written to {output_file}")
    else:
        click.echo(report)

    # Exit code
    has_failures = any(r.status == "failed" for r in results)
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
