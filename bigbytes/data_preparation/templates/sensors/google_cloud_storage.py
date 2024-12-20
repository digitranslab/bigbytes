from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.google_cloud_storage import GoogleCloudStorage
from os import path

if 'sensor' not in globals():
    from bigbytes.data_preparation.decorators import sensor


@sensor
def check_condition(*args, **kwargs) -> bool:
    """
    Template code for checking if a file or folder exists in a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.ai/design/data-loading#googlecloudstorage
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'your_bucket_name'
    object_key = 'your_object_key'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).exists(
        bucket_name,
        object_key,
    )
