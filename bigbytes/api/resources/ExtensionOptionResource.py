from bigbytes.api.errors import ApiError
from bigbytes.api.resources.GenericResource import GenericResource
from bigbytes.extensions.constants import EXTENSIONS, EXTENSIONS_BY_UUID
from bigbytes.orchestration.db import safe_db_query


class ExtensionOptionResource(GenericResource):
    @classmethod
    @safe_db_query
    def collection(self, query, meta, user, **kwargs):
        return self.build_result_set(
            EXTENSIONS,
            user,
            **kwargs,
        )

    @classmethod
    @safe_db_query
    def member(self, pk, user, **kwargs):
        model = EXTENSIONS_BY_UUID.get(pk)
        if not model:
            raise ApiError(ApiError.RESOURCE_NOT_FOUND)

        return self(model, user, **kwargs)
