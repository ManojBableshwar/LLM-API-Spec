"""Tests for the CLI module."""

from __future__ import annotations

import json
import os
import tempfile

import pytest
from click.testing import CliRunner

from llm_api_spec.cli import main, _resolve_env_vars, _parse_capabilities
from llm_api_spec.models import Capability


class TestResolveEnvVars:
    def test_simple_var(self):
        os.environ["TEST_VAR_XYZ"] = "resolved"
        assert _resolve_env_vars("prefix-${TEST_VAR_XYZ}-suffix") == "prefix-resolved-suffix"
        del os.environ["TEST_VAR_XYZ"]

    def test_unset_var(self):
        result = _resolve_env_vars("${NONEXISTENT_VAR_12345}")
        assert result == "${NONEXISTENT_VAR_12345}"

    def test_no_vars(self):
        assert _resolve_env_vars("plain text") == "plain text"

    def test_multiple_vars(self):
        os.environ["VAR_A"] = "a"
        os.environ["VAR_B"] = "b"
        assert _resolve_env_vars("${VAR_A}-${VAR_B}") == "a-b"
        del os.environ["VAR_A"]
        del os.environ["VAR_B"]

    def test_non_string(self):
        assert _resolve_env_vars(123) == 123


class TestParseCapabilities:
    def test_all(self):
        assert _parse_capabilities("all") is None

    def test_single(self):
        result = _parse_capabilities("text_input")
        assert result == [Capability.TEXT_INPUT]

    def test_multiple(self):
        result = _parse_capabilities("text_input,text_output")
        assert result == [Capability.TEXT_INPUT, Capability.TEXT_OUTPUT]

    def test_unknown(self):
        with pytest.raises(Exception):
            _parse_capabilities("nonexistent_cap")


class TestCLI:
    def test_no_args(self):
        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code != 0
        assert "Either --config or --target is required" in result.output

    def test_target_without_model(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--target", "https://example.com/v1"])
        assert result.exit_code != 0
        assert "--model is required" in result.output

    def test_config_file_not_found(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--config", "/nonexistent/config.yaml"])
        assert result.exit_code != 0
        assert "Config file not found" in result.output

    def test_valid_config_file(self):
        config = {
            "targets": [
                {
                    "name": "test",
                    "base_url": "https://example.com/v1",
                    "model": "test-model",
                    "schemas": ["chat_completions"],
                }
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            import yaml
            yaml.dump(config, f)
            f.flush()

            runner = CliRunner()
            # This will fail because the endpoint doesn't exist, but config parsing should work
            result = runner.invoke(main, ["--config", f.name, "--capabilities", "text_input"])
            # We expect a connection error, not a config error
            assert "Config file not found" not in (result.output or "")
            os.unlink(f.name)
