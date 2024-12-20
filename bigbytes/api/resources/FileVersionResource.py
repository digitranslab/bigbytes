from bigbytes.api.errors import ApiError
from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.data_preparation.models.block import Block
from bigbytes.data_preparation.models.file import File
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.orchestration.db import safe_db_query
from bigbytes.settings.repo import get_repo_path


class FileVersionResource(GenericResource):
    @classmethod
    @safe_db_query
    def collection(self, query, meta, user, **kwargs):
        parent_model = kwargs.get('parent_model')

        pipeline_uuid = query.get('pipeline_uuid', [False])
        if pipeline_uuid:
            pipeline_uuid = pipeline_uuid[0]

        block_uuid = query.get('block_uuid', [False])
        if block_uuid:
            block_uuid = block_uuid[0]

        if pipeline_uuid and block_uuid:
            repo_path = get_repo_path(user=user)
            pipeline = Pipeline.get(pipeline_uuid, repo_path=repo_path)
            if pipeline:
                block = pipeline.get_block(block_uuid)
                if block:
                    parent_model = block.file

        if isinstance(parent_model, Block):
            pass
        elif isinstance(parent_model, File):
            return self.build_result_set(
                parent_model.file_versions(),
                user,
                **kwargs,
            )
        else:
            raise ApiError(ApiError.RESOURCE_INVALID.copy())
