from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.FolderPresenter import FolderPresenter


class FolderPolicy(BasePolicy):
    pass


FolderPolicy.allow_actions([
    constants.CREATE,
    constants.DELETE,
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())

FolderPolicy.allow_read(FolderPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
    constants.DELETE,
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

FolderPolicy.allow_write([
    'name',
    'overwrite',
    'path',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())

FolderPolicy.allow_write([
    'name',
    'path',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_editor_role_and_pipeline_edit_access())
