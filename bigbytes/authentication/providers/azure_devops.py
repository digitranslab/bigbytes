from bigbytes.authentication.oauth.constants import ProviderName
from bigbytes.authentication.providers.active_directory import ADProvider
from bigbytes.settings import get_settings_value
from bigbytes.settings.keys import AZURE_DEVOPS_ORGANIZATION


class AzureDevopsProvider(ADProvider):
    provider = ProviderName.AZURE_DEVOPS
    # This is a hardcoded scope value that is used to get Git access to the Azure DevOps project.
    # This should not be changed unless this scope stops working properly.
    scope = '499b84ac-1321-427f-aa17-267ca6975798/.default'

    def __init__(self):
        super().__init__()
        if not get_settings_value(AZURE_DEVOPS_ORGANIZATION):
            raise Exception(
                'Azure DevOps organization is empty. '
                'Make sure the AZURE_DEVOPS_ORGANIZATION environment variable is set.')
