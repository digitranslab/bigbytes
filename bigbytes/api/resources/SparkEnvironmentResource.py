from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.api.resources.mixins.spark import SparkApplicationChild


class SparkEnvironmentResource(GenericResource, SparkApplicationChild):
    @classmethod
    async def member(self, _pk, user, **kwargs):
        return self(
            await self.build_api().environment(),
            user,
            **kwargs,
        )
