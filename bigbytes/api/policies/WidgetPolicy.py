from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.WidgetPresenter import WidgetPresenter
from bigbytes.data_preparation.repo_manager import get_project_uuid
from bigbytes.orchestration.constants import Entity


class WidgetPolicy(BasePolicy):
    @property
    def entity(self):
        parent_model = self.options.get('parent_model')
        if parent_model:
            return Entity.PIPELINE, parent_model.uuid

        return Entity.PROJECT, get_project_uuid()


WidgetPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

WidgetPolicy.allow_actions([
    constants.CREATE,
    constants.DELETE,
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())

WidgetPolicy.allow_read(WidgetPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

WidgetPolicy.allow_read(WidgetPresenter.default_attributes + [
    'retry_config',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.DELETE,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())

WidgetPolicy.allow_write([
    'all_upstream_blocks_executed',
    'color',
    'config',
    'configuration',
    'content',
    'downstream_blocks',
    'executor_config',
    'executor_type',
    'has_callback',
    'language',
    'name',
    'priority',
    'retry_config',
    'status',
    'timeout',
    'type',
    'upstream_blocks',
    'uuid',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())
