import json
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union

from ldap3 import Connection, Server
from ldap3.core.exceptions import LDAPException

from bigbytes.data_preparation.repo_manager import get_repo_config
from bigbytes.settings import get_settings_value
from bigbytes.settings.keys import (
    LDAP_AUTHENTICATION_FILTER,
    LDAP_AUTHORIZATION_FILTER,
    LDAP_BASE_DN,
    LDAP_BIND_DN,
    LDAP_BIND_PASSWORD,
    LDAP_GROUP_FIELD,
    LDAP_ROLES_MAPPING,
    LDAP_SERVER,
)
from bigbytes.shared.hash import merge_dict


class LDAPAuthenticator(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> Tuple[bool, str, Dict]:
        pass

    @abstractmethod
    def authorize(self, username: str) -> bool:
        pass

    def verify(self, username: str, password: str) -> bool:
        authenticated, user_dn, user_attributes = self.authenticate(username, password)
        if authenticated:
            return self.authorize(user_dn)
        return False


class LDAPConnection(LDAPAuthenticator):
    def __init__(
        self,
        server_url: str,
        bind_dn: str,
        bind_password: str,
        base_dn: str,
        authentication_filter: str,
        authorization_filter: str,
        group_field: str = None,
        roles_mapping: Union[Dict, str] = None,
    ):
        self.server_url = server_url
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.base_dn = base_dn
        self.authentication_filter = authentication_filter
        self.authorization_filter = authorization_filter
        self.group_field = group_field

        if type(roles_mapping) is str:
            try:
                self.roles_mapping = json.loads(roles_mapping)
            except json.JSONDecodeError:
                self.roles_mapping = None
        else:
            self.roles_mapping = roles_mapping

        self.conn = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.unbind()

    def bind(self):
        self.conn = Connection(
            Server(self.server_url), self.bind_dn, self.bind_password, auto_bind=True
        )

    def authenticate(self, username: str, password: str) -> Tuple[bool, str, Dict]:
        try:
            if not self.conn:
                self.bind()
            self.conn.search(
                self.base_dn,
                self.authentication_filter.format(username=username),
                attributes=[self.group_field] if self.group_field else None,
            )
            if not self.conn.entries:
                return False, "", dict()
            user_dn = self.conn.entries[0].entry_dn
            user_attributes = self.conn.entries[0].entry_attributes_as_dict
            if self.conn.rebind(user=user_dn, password=password):
                return True, user_dn, user_attributes
            return False, user_dn, user_attributes
        except LDAPException:
            return False, "", dict()

    def authorize(self, username: str) -> bool:
        try:
            if not self.conn:
                self.bind()
            self.conn.entries.clear()
            self.conn.search(self.base_dn, self.authorization_filter.format(user_dn=username))
            if self.conn.entries:
                if len(self.conn.entries) > 0:
                    return True
            return False
        except LDAPException:
            return False

    def get_user_roles(self, user_attributes: Dict[str, List]) -> List[str]:
        if not self.roles_mapping:
            return []
        groups = user_attributes.get(self.group_field, [])
        roles = set()
        for group in groups:
            if group in self.roles_mapping:
                roles.update(self.roles_mapping[group])
            else:
                print(f"Can't find group {group} in LDAP role mapping")
        return list(roles)


def new_ldap_connection() -> LDAPConnection:
    ldap_config_from_env_vars = dict(
        server_url=get_settings_value(LDAP_SERVER, 'ldaps://127.0.0.1:1636'),
        bind_dn=get_settings_value(LDAP_BIND_DN, 'cd=admin,dc=example,dc=org'),
        bind_password=get_settings_value(LDAP_BIND_PASSWORD, 'admin_password'),
        base_dn=get_settings_value(LDAP_BASE_DN, 'dc=example,dc=org'),
        authentication_filter=get_settings_value(
            LDAP_AUTHENTICATION_FILTER,
            '(&(|(objectClass=Pers)(objectClass=gro))(cn={username}))'
        ),
        authorization_filter=get_settings_value(
            LDAP_AUTHORIZATION_FILTER,
            '(&(objectClass=groupOfNames)(cn=group)(member={user_dn}))'
        ),
        group_field=get_settings_value(
            LDAP_GROUP_FIELD,
            'memberOf',
        ),
        roles_mapping=get_settings_value(LDAP_ROLES_MAPPING),
    )
    try:
        ldap_config = get_repo_config().ldap_config
    except Exception:
        ldap_config = dict()
    merged = merge_dict(ldap_config_from_env_vars, ldap_config)

    return LDAPConnection(**merged)


def verify(username, password: str) -> bool:
    return new_ldap_connection().verify(username, password)
