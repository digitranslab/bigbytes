from typing import Dict, List, Union

from bigbytes.orchestration.db.models.schedules import PipelineSchedule
from bigbytes.presenters.pages.loaders.base import BaseLoader


class Loader(BaseLoader):
    @classmethod
    async def load(
        self,
        ids: List[Union[int, str]],
        query: Dict = None,
        **kwargs,
    ) -> List[PipelineSchedule]:
        if ids:
            ids = list(filter(lambda x: x, ids))

        if ids:
            return PipelineSchedule.query.filter(
                PipelineSchedule.id.in_(ids),
            ).all()

        return []
