from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.PipelinePresenter import PipelinePresenter
from bigbytes.data_preparation.repo_manager import get_project_uuid
from bigbytes.orchestration.constants import Entity


class PipelinePolicy(BasePolicy):
    @property
    def entity(self):
        if self.resource and self.resource.model:
            return Entity.PIPELINE, self.resource.model.uuid

        return Entity.PROJECT, get_project_uuid()


PipelinePolicy.allow_actions(
    [
        constants.DETAIL,
        constants.LIST,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelinePolicy.allow_actions(
    [
        constants.CREATE,
        constants.DELETE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)

PipelinePolicy.allow_actions(
    [
        constants.UPDATE,
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
)

PipelinePolicy.allow_read(
    PipelinePresenter.default_attributes
    + [
        'callbacks',
        'conditionals',
        'extensions',
        'schedules',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.DETAIL,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelinePolicy.allow_read(
    PipelinePresenter.default_attributes
    + [
        'callbacks',
        'conditionals',
        'extensions',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.CREATE,
        constants.DELETE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)

PipelinePolicy.allow_read(
    PipelinePresenter.default_attributes
    + [
        'callbacks',
        'conditionals',
        'extensions',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
)

PipelinePolicy.allow_read(
    PipelinePresenter.default_attributes
    + [
        'callbacks',
        'conditionals',
        'extensions',
        'history',
        'operation_history',
        'schedules',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelinePolicy.allow_write(
    [
        'callbacks',
        'conditionals',
        'clone_pipeline_uuid',
        'custom_template_uuid',
        'description',
        'extensions',
        'llm',
        'name',
        'tags',
        'type',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.CREATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)

PipelinePolicy.allow_write(
    [
        'add_upstream_for_block_uuid',
        'callbacks',
        'conditionals',
        'extensions',
        'llm',
        'schedules',
    ]
    + PipelinePresenter.default_attributes,
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)

PipelinePolicy.allow_write(
    [
        'pipeline_runs',
        'pipeline_schedule_id',
        'status',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role(),
)

PipelinePolicy.allow_query(
    [
        'include_block_pipelines',
        'include_schedules',
        'includes_block_metadata',
        'includes_content',
        'includes_extensions',
        'includes_outputs',
        'max_results_for_block_outputs',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.DETAIL,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelinePolicy.allow_query(
    [
        'includes_outputs_spark',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.DETAIL,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
    override_permission_condition=lambda _policy: True,
)

PipelinePolicy.allow_query(
    [
        'from_history_days',
        'include_schedules',
        'repo_path',
        'search',
        'status[]',
        'tag[]',
        'type[]',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.LIST,
    ],
    condition=lambda policy: policy.has_at_least_viewer_role(),
)

PipelinePolicy.allow_query(
    [
        'update_content',
    ],
    scopes=[
        OauthScope.CLIENT_PRIVATE,
    ],
    on_action=[
        constants.UPDATE,
    ],
    condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access(),
)
