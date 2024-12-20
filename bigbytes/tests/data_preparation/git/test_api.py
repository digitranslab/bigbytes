from datetime import timedelta

from faker import Faker

from bigbytes.authentication.oauth2 import generate_access_token
from bigbytes.authentication.oauth.constants import ProviderName
from bigbytes.data_preparation.git.api import (
    get_access_token_for_user,
    get_oauth_client_id,
)
from bigbytes.orchestration.db.models.oauth import Oauth2Application
from bigbytes.tests.base_test import DBTestCase
from bigbytes.tests.factory import create_user


class GitApiTest(DBTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def test_get_access_token_for_user(self):
        email = self.faker.email()
        user = create_user(email=email, roles=1)

        client_id = get_oauth_client_id(ProviderName.GITHUB)

        oauth_client = Oauth2Application.create(
            client_id=client_id,
            client_type=Oauth2Application.ClientType.PRIVATE,
            name=ProviderName.GITHUB,
            user_id=user.id if user else None,
        )

        generate_access_token(
            user,
            application=oauth_client,
            duration=int(timedelta(days=30).total_seconds()),
        )

        access_token = get_access_token_for_user(user, provider=ProviderName.GITHUB)
        self.assertIsNotNone(access_token)
