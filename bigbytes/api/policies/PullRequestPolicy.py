from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.presenters.PullRequestPresenter import PullRequestPresenter


class PullRequestPolicy(BasePolicy):
    pass


PullRequestPolicy.allow_actions([
    constants.DETAIL,
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


PullRequestPolicy.allow_actions([
    constants.DETAIL,
    constants.LIST,
    constants.CREATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_editor_role())


PullRequestPolicy.allow_read(PullRequestPresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE
], on_action=[
    constants.DETAIL,
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())


PullRequestPolicy.allow_read(PullRequestPresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_editor_role())


PullRequestPolicy.allow_write([
    'base_branch',
    'body',
    'compare_branch',
    'remote_url',
    'repository',
    'title',
], scopes=[
    OauthScope.CLIENT_PRIVATE
], on_action=[
    constants.CREATE,
], condition=lambda policy: policy.has_at_least_editor_role())


PullRequestPolicy.allow_query([
    'repository',
    'remote_url',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
