import time
import traceback
from dataclasses import dataclass, field
from typing import Dict, List

import pandas as pd

from bigbytes.io.base import ExportWritePolicy
from bigbytes.io.constants import UNIQUE_CONFLICT_METHOD_IGNORE
from bigbytes.io.postgres import Postgres
from bigbytes.shared.config import BaseConfig
from bigbytes.streaming.sinks.base import BaseSink


@dataclass
class PostgresConfig(BaseConfig):
    database: str
    host: str
    password: str
    schema: str
    table: str
    username: str
    port: int = 5432
    unique_conflict_method: str = UNIQUE_CONFLICT_METHOD_IGNORE
    unique_constraints: List = field(default_factory=list)
    allow_reserved_words: bool = False
    auto_clean_name: bool = True
    case_sensitive: bool = False


class PostgresSink(BaseSink):
    config_class = PostgresConfig

    def init_client(self):
        # Initialize postgres connection
        self.postgres_client = Postgres(
            dbname=self.config.database,
            user=self.config.username,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
            schema=self.config.schema,
        )
        self.postgres_client.open()

    def write(self, message: Dict):
        self.batch_write([message])

    def batch_write(self, messages: List[Dict]):
        if not messages:
            return
        self._print(
            f'Batch ingest {len(messages)} records, time={time.time()}. Sample: {messages[0]}')

        df = pd.DataFrame.from_records(messages)
        self.postgres_client.export(
            df,
            self.config.schema,
            self.config.table,
            if_exists=ExportWritePolicy.APPEND,
            unique_conflict_method=self.config.unique_conflict_method,
            unique_constraints=self.config.unique_constraints,
            allow_reserved_words=self.config.allow_reserved_words,
            auto_clean_name=self.config.auto_clean_name,
            case_sensitive=self.config.case_sensitive,
        )

    def destroy(self):
        try:
            self.postgres_client.close()
        except Exception:
            traceback.print_exc()
