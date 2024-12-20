from os import path

from pandas import DataFrame

from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.weaviate import Weaviate

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_weaviate(df: DataFrame, **kwargs) -> None:
    """
    Template to export data to Weaviate.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    new_collection = 'Test'

    Weaviate.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        collection=new_collection
    )
