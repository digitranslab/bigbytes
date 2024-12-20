from functools import reduce
from typing import Dict

from bigbytes.presenters.pages.models.client_pages.pipeline_schedules import (
    CreatePage as PipelineSchedulesCreatePage,
)
from bigbytes.presenters.pages.models.client_pages.pipeline_schedules import (
    ListPage as PipelineSchedulesListPage,
)
from bigbytes.presenters.pages.models.client_pages.pipelines import (
    DetailPage as PipelinesDetailPage,
)
from bigbytes.presenters.pages.models.client_pages.pipelines import (
    ListPage as PipelinesListPage,
)


def _combine(acc, model) -> Dict:
    acc[model.get_uuid()] = model
    return acc


CLIENT_PAGES = reduce(_combine, [
    PipelineSchedulesCreatePage,
    PipelineSchedulesListPage,
    PipelinesDetailPage,
    PipelinesListPage,
], {})
