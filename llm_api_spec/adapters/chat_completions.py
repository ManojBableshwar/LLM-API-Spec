"""Chat Completions schema adapter (/v1/chat/completions)."""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

from llm_api_spec.adapters.base import SchemaAdapter
from llm_api_spec.models import (
    NormalizedResponse,
    NormalizedToolCall,
    NormalizedUsage,
    SchemaType,
)


class ChatCompletionsAdapter(SchemaAdapter):
    schema_type = SchemaType.CHAT_COMPLETIONS

    def endpoint_path(self) -> str:
        return "/chat/completions"

    def build_request(self, **kwargs: Any) -> dict[str, Any]:
        messages = kwargs.get("messages")
        if messages is None:
            prompt = kwargs.get("prompt", "Hello")
            messages = [{"role": "user", "content": prompt}]

        body: dict[str, Any] = {
            "model": self.target.model,
            "messages": messages,
        }

        optional_keys = [
            "tools",
            "tool_choice",
            "parallel_tool_calls",
            "response_format",
            "stream",
            "stop",
            "logprobs",
            "top_logprobs",
            "seed",
            "max_completion_tokens",
            "temperature",
        ]
        for key in optional_keys:
            if key in kwargs:
                body[key] = kwargs[key]

        # Translate legacy max_tokens to max_completion_tokens
        if "max_tokens" in kwargs and "max_completion_tokens" not in kwargs:
            body["max_completion_tokens"] = kwargs["max_tokens"]

        return body

    def parse_response(self, response_data: dict[str, Any]) -> dict[str, Any]:
        parsed: dict[str, Any] = {
            "id": response_data.get("id"),
            "model": response_data.get("model"),
            "object": response_data.get("object"),
        }

        choices = response_data.get("choices", [])
        if choices:
            choice = choices[0]
            message = choice.get("message", {})
            parsed["content"] = message.get("content")
            parsed["role"] = message.get("role")
            parsed["finish_reason"] = choice.get("finish_reason")
            parsed["tool_calls"] = message.get("tool_calls")
        else:
            parsed["content"] = None
            parsed["role"] = None
            parsed["finish_reason"] = None
            parsed["tool_calls"] = None

        parsed["usage"] = response_data.get("usage")
        return parsed

    def normalize(self, response_data: dict[str, Any]) -> NormalizedResponse:
        choices = response_data.get("choices", [])
        text = None
        tool_calls: list[NormalizedToolCall] = []
        finish_reason = None

        if choices:
            choice = choices[0]
            message = choice.get("message", {})
            text = message.get("content")
            finish_reason = choice.get("finish_reason")

            raw_tool_calls = message.get("tool_calls") or []
            for tc in raw_tool_calls:
                func = tc.get("function", {})
                tool_calls.append(
                    NormalizedToolCall(
                        id=tc.get("id"),
                        name=func.get("name", ""),
                        arguments=func.get("arguments", "{}"),
                    )
                )

        usage = None
        raw_usage = response_data.get("usage")
        if raw_usage:
            usage = NormalizedUsage(
                prompt_tokens=raw_usage.get("prompt_tokens"),
                completion_tokens=raw_usage.get("completion_tokens"),
                total_tokens=raw_usage.get("total_tokens"),
            )

        return NormalizedResponse(
            text=text,
            tool_calls=tool_calls,
            finish_reason=finish_reason,
            model=response_data.get("model"),
            usage=usage,
            response_id=response_data.get("id"),
        )

    async def stream_response(
        self, request_body: dict[str, Any]
    ) -> AsyncIterator[dict[str, Any]]:
        request_body = {**request_body, "stream": True}
        client = await self.get_client()
        async with client.stream(
            "POST", self.endpoint_path(), json=request_body
        ) as response:
            response.raise_for_status()
            buffer = ""
            async for chunk in response.aiter_text():
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    if line == "data: [DONE]":
                        return
                    if line.startswith("data: "):
                        data_str = line[6:]
                        try:
                            yield json.loads(data_str)
                        except json.JSONDecodeError:
                            continue
