from bigbytes.shared.enum import StrEnum


class LLMUseCase(StrEnum):
    GENERATE_DOC_FOR_BLOCK = 'generate_doc_for_block'
    GENERATE_DOC_FOR_PIPELINE = 'generate_doc_for_pipeline'
    GENERATE_BLOCK_WITH_DESCRIPTION = 'generate_block_with_description'
    GENERATE_CODE = 'generate_code'
    GENERATE_PIPELINE_WITH_DESCRIPTION = 'generate_pipeline_with_description'
    GENERATE_COMMENT_FOR_CODE = 'generate_comment_for_code'
