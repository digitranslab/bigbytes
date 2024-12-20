from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.TagPresenter import TagPresenter


class TagPolicy(BasePolicy):
    pass


TagPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

TagPolicy.allow_actions([
    constants.CREATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role())

TagPolicy.allow_read(TagPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

TagPolicy.allow_read(TagPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_editor_role())

TagPolicy.allow_write(TagPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_editor_role())
