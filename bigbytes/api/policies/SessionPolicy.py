from typing import Dict

from bigbytes.api.constants import AttributeOperationType
from bigbytes.api.oauth_scope import OauthScope
from bigbytes.api.operations import constants
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.policies.BasePolicy import BasePolicy
from bigbytes.api.policies.mixins.user_permissions import UserPermissionMixIn
from bigbytes.orchestration.constants import Entity
from bigbytes.shared.hash import merge_dict


class SessionPolicy(BasePolicy, UserPermissionMixIn):
    @classmethod
    def action_rule_with_permissions(self, operation: OperationType) -> Dict:
        return merge_dict(super().action_rule_with_permissions(operation), {
            OauthScope.CLIENT_PUBLIC: [
                dict(
                    condition=lambda _policy: OperationType.CREATE == operation,
                ),
            ],
        })

    @classmethod
    def attribute_rule_with_permissions(
        self,
        attribute_operation_type: AttributeOperationType,
        resource_attribute: str,
    ) -> Dict:
        config = {}
        if AttributeOperationType.READ == attribute_operation_type:
            config = self.read_rules[self.__name__].get(resource_attribute)
        else:
            config = self.write_rules[self.__name__].get(resource_attribute)

        return merge_dict(super().attribute_rule_with_permissions(
            attribute_operation_type,
            resource_attribute,
        ), {
            OauthScope.CLIENT_PUBLIC: {
                OperationType.CREATE: config[OauthScope.CLIENT_PUBLIC][OperationType.CREATE],
            },
        })

    @property
    def entity(self):
        return Entity.ANY, None


SessionPolicy.allow_actions([
    constants.CREATE,
], scopes=[
    OauthScope.CLIENT_PUBLIC,
])

SessionPolicy.allow_actions([
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

SessionPolicy.allow_read([
    'expires',
    'token',
    'user',
], scopes=[
    OauthScope.CLIENT_PUBLIC,
], on_action=[
    constants.CREATE,
])

SessionPolicy.allow_read([
    'expires',
    'token',
    'user',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

SessionPolicy.allow_write([
    'email',
    'password',
    'username',
    'token',
    'provider',
], scopes=[
    OauthScope.CLIENT_PUBLIC,
], on_action=[
    constants.CREATE,
])
