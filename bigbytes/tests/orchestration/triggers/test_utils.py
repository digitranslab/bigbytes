import os

from bigbytes.data_preparation.models.block import Block
from bigbytes.data_preparation.models.constants import BlockType
from bigbytes.data_preparation.models.global_data_product import GlobalDataProduct
from bigbytes.data_preparation.models.pipeline import Pipeline
from bigbytes.orchestration.db.models.schedules import PipelineRun
from bigbytes.orchestration.triggers.global_data_product import (
    fetch_or_create_pipeline_schedule,
)
from bigbytes.orchestration.triggers.utils import (
    check_pipeline_run_status,
    create_and_start_pipeline_run,
)
from bigbytes.tests.base_test import DBTestCase


class TriggerUtilsTest(DBTestCase):
    def setUp(self):
        super().setUp()

        try:
            self.pipeline = Pipeline.create(
                'test pipeline',
                repo_path=self.repo_path,
            )
            self.pipeline.add_block(Block('data_loader', 'data_loader', BlockType.DATA_LOADER))
            self.pipeline.add_block(Block('transformer', 'transformer', BlockType.TRANSFORMER))
            self.pipeline.add_block(
                Block('data_exporter', 'data_exporter', BlockType.DATA_EXPORTER))
        except Exception:
            self.pipeline = Pipeline.get('test_pipeline', repo_path=self.repo_path)

        self.global_data_product = GlobalDataProduct(
            object_type='pipeline',
            object_uuid=self.pipeline.uuid,
            outdated_after=dict(
                months=1,
                seconds=2,
                weeks=3,
                years=4,
            ),
            outdated_starting_at=dict(
                day_of_month=1,
                day_of_week=2,
                day_of_year=3,
                hour_of_day=4,
                minute_of_hour=5,
                month_of_year=6,
                second_of_minute=7,
                week_of_month=8,
                week_of_year=9,
            ),
            repo_path=self.repo_path,
            settings=dict(
                data_exporter={},
                data_loader=dict(partitions=1),
                transformer=dict(partitions=2),
            ),
            uuid='bigbytes',
        )
        self.pipeline_schedule = fetch_or_create_pipeline_schedule(self.global_data_product)

        self.file_path = os.path.join(
            self.repo_path,
            'global_data_products.yaml',
        )
        self.global_data_product.save()

    def tearDown(self):
        super().tearDown()
        os.remove(self.file_path)

    def test_check_pipeline_run_status(self):
        pipeline_run = create_and_start_pipeline_run(
            self.pipeline,
            self.pipeline_schedule,
            dict(variables=dict(bigbytes=3)),
        )

        error = False
        try:
            check_pipeline_run_status(pipeline_run, poll_interval=1, poll_timeout=1)
        except Exception:
            error = True
        self.assertTrue(error)

        pipeline_run.status = PipelineRun.PipelineRunStatus.FAILED
        pipeline_run.save()

        error = False
        try:
            check_pipeline_run_status(pipeline_run, error_on_failure=True)
        except Exception as err:
            error = True
            self.assertEqual(
                f'Pipeline run {pipeline_run.id} for pipeline {self.pipeline.uuid}: failed.',
                str(err),
            )
        self.assertTrue(error)

        pipeline_run.status = PipelineRun.PipelineRunStatus.CANCELLED
        pipeline_run.save()
        check_pipeline_run_status(pipeline_run, error_on_failure=True)

        pipeline_run.status = PipelineRun.PipelineRunStatus.COMPLETED
        pipeline_run.save()
        check_pipeline_run_status(pipeline_run, error_on_failure=True)

    def test_create_and_start_pipeline_run(self):
        pipeline_run = create_and_start_pipeline_run(
            self.pipeline,
            self.pipeline_schedule,
            dict(variables=dict(bigbytes=3)),
        )

        self.assertEqual(pipeline_run.pipeline_schedule, self.pipeline_schedule)
        self.assertEqual(pipeline_run.variables['bigbytes'], 3)
