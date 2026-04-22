from llm_api_spec.checks.basic_text import check_text_input, check_text_output
from llm_api_spec.checks.tool_calling import (
    check_tool_calling,
    check_tool_choice_auto,
    check_tool_choice_none,
    check_tool_choice_required,
    check_tool_choice_function,
    check_multiple_tool_calls,
    check_parallel_tool_calls,
)
from llm_api_spec.checks.structured_output import (
    check_json_output,
    check_structured_output,
    check_json_schema_constraints,
    check_regex_constraints,
    check_grammar_constraints,
)
from llm_api_spec.checks.multimodal import (
    check_image_input_url,
    check_image_input_base64,
    check_image_input_multi,
    check_image_output,
)
from llm_api_spec.checks.file_input import (
    check_file_input_inline,
    check_file_input_reference,
)
from llm_api_spec.checks.lifecycle import (
    check_previous_response_id,
    check_background_mode,
    check_response_retrieval,
    check_built_in_tools,
)
from llm_api_spec.checks.streaming import check_streaming
from llm_api_spec.checks.logprobs import check_logprobs
from llm_api_spec.checks.determinism import check_seeded_determinism
from llm_api_spec.checks.long_context import check_long_prompt_acceptance
from llm_api_spec.checks.normalization import check_normalization

from llm_api_spec.models import Capability

CAPABILITY_CHECK_MAP: dict[Capability, object] = {
    Capability.TEXT_INPUT: check_text_input,
    Capability.TEXT_OUTPUT: check_text_output,
    Capability.JSON_OUTPUT: check_json_output,
    Capability.STRUCTURED_OUTPUT: check_structured_output,
    Capability.TOOL_CALLING: check_tool_calling,
    Capability.TOOL_CHOICE_AUTO: check_tool_choice_auto,
    Capability.TOOL_CHOICE_NONE: check_tool_choice_none,
    Capability.TOOL_CHOICE_REQUIRED: check_tool_choice_required,
    Capability.TOOL_CHOICE_FUNCTION: check_tool_choice_function,
    Capability.MULTIPLE_TOOL_CALLS: check_multiple_tool_calls,
    Capability.PARALLEL_TOOL_CALLS: check_parallel_tool_calls,
    Capability.IMAGE_INPUT_URL: check_image_input_url,
    Capability.IMAGE_INPUT_BASE64: check_image_input_base64,
    Capability.IMAGE_INPUT_MULTI: check_image_input_multi,
    Capability.IMAGE_OUTPUT: check_image_output,
    Capability.FILE_INPUT_INLINE: check_file_input_inline,
    Capability.FILE_INPUT_REFERENCE: check_file_input_reference,
    Capability.BUILT_IN_TOOLS: check_built_in_tools,
    Capability.STREAMING: check_streaming,
    Capability.STOP_SEQUENCES: check_text_input,  # placeholder, replaced below
    Capability.LOGPROBS: check_logprobs,
    Capability.SEEDED_DETERMINISM: check_seeded_determinism,
    Capability.LONG_PROMPT_ACCEPTANCE: check_long_prompt_acceptance,
    Capability.PREVIOUS_RESPONSE_ID: check_previous_response_id,
    Capability.BACKGROUND_MODE: check_background_mode,
    Capability.RESPONSE_RETRIEVAL: check_response_retrieval,
    Capability.NORMALIZATION: check_normalization,
    Capability.REGEX_CONSTRAINTS: check_regex_constraints,
    Capability.GRAMMAR_CONSTRAINTS: check_grammar_constraints,
    Capability.JSON_SCHEMA_CONSTRAINTS: check_json_schema_constraints,
}

# Fix stop_sequences mapping
from llm_api_spec.checks.basic_text import check_stop_sequences
CAPABILITY_CHECK_MAP[Capability.STOP_SEQUENCES] = check_stop_sequences

__all__ = ["CAPABILITY_CHECK_MAP"]
