from typing import Dict

from bigbytes.api.resources.AsyncBaseResource import AsyncBaseResource
from bigbytes.data_preparation.models.project import Project
from bigbytes.data_preparation.models.project.constants import FeatureUUID
from bigbytes.presenters.design.models import CustomDesign


class CustomDesignResource(AsyncBaseResource):
    @classmethod
    async def collection(self, query: Dict, _meta: Dict, user, **kwargs):
        results = []

        if Project.is_feature_enabled_in_root_or_active_project(FeatureUUID.CUSTOM_DESIGN):
            results = CustomDesign.get_all()

        return self.build_result_set(results, user, **kwargs)

    @classmethod
    async def member(self, pk, user, **kwargs):
        model = CustomDesign()

        if Project.is_feature_enabled_in_root_or_active_project(FeatureUUID.CUSTOM_DESIGN):
            model = CustomDesign.combine_in_order_of_priority()

        return self(model, user, **kwargs)
