from bigbytes.io.file import FileIO
from pandas import DataFrame

if 'data_exporter' not in globals():
    from bigbytes.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_file(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to filesystem.

    Docs: https://docs.bigbytes.io/design/data-loading#fileio
    """
    filepath = 'path/to/write/dataframe/to.csv'
    FileIO().export(df, filepath)