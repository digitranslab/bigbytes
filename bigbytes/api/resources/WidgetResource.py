import asyncio
from typing import Dict

from bigbytes.api.errors import ApiError
from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.data_preparation.models.widget import Widget
from bigbytes.orchestration.db import safe_db_query
from bigbytes.settings.repo import get_repo_path


class WidgetResource(GenericResource):
    @classmethod
    @safe_db_query
    async def collection(self, query, meta, user, **kwargs):
        pipeline = kwargs['parent_model']

        include_outputs = query.get('include_outputs', [True])
        if include_outputs:
            include_outputs = include_outputs[0]

        collection = await asyncio.gather(
            *[widget.to_dict_async(
                include_content=True,
                include_outputs=include_outputs,
              ) for widget in pipeline.widgets_by_uuid.values()]
        )

        return self.build_result_set(
            collection,
            user,
            **kwargs,
        )

    @classmethod
    @safe_db_query
    async def create(self, payload: Dict, user, **kwargs) -> 'WidgetResource':
        pipeline = kwargs['parent_model']

        resource = Widget.create(
            payload.get('name') or payload.get('uuid'),
            payload.get('type'),
            get_repo_path(user=user),
            config=payload.get('config'),
            language=payload.get('language'),
            pipeline=pipeline,
            priority=payload.get('priority'),
            upstream_block_uuids=payload.get('upstream_blocks', []),
        )

        if payload.get('content'):
            await resource.update_content_async(payload['content'], widget=True)

        if payload.get('configuration'):
            resource.configuration = payload['configuration']
            pipeline.save()

        return self(resource, user, **kwargs)

    @classmethod
    @safe_db_query
    async def member(self, pk, user, **kwargs):
        pipeline = kwargs['parent_model']
        widget = pipeline.get_block(pk, widget=True)

        error = ApiError.RESOURCE_NOT_FOUND.copy()
        if widget is None:
            error.update(message=f'Widget {pk} does not exist in pipeline {pipeline.uuid}.')
            raise ApiError(error)

        return self(widget, user, **kwargs)

    @safe_db_query
    def delete(self, **kwargs):
        self.model.delete()
        return self

    @safe_db_query
    def update(self, payload, **kwargs):
        self.model.update(payload)
        if payload.get('configuration'):
            self.model.configuration = payload['configuration']
            self.parent_model().save()
        return self
