from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.redshift import Redshift
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_redshift(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Redshift cluster.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.ai/design/data-loading#redshift
    """
    table_name = 'your_table_name'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Redshift.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            table_name,
            if_exists='replace',  # Specify resolution policy if table already exists
        )
