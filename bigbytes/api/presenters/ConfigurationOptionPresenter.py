from typing import Dict

from bigbytes.api.presenters.BasePresenter import BasePresenter


class ConfigurationOptionPresenter(BasePresenter):
    default_attributes = [
        'configuration_type',
        'metadata',
        'option',
        'option_type',
        'resource_type',
        'uuid',
    ]

    async def prepare_present(self, **kwargs) -> Dict:
        return self.resource.model.to_dict()
