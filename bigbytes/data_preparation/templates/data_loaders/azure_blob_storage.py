{% extends "data_loaders/default.jinja" %}
{% block imports %}
from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.azure_blob_storage import AzureBlobStorage
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_from_azure_blob_storage(*args, **kwargs):
    """
    Template for loading data from a Azure Blob Storage.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.ai/design/data-loading#azureblobstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    container_name = 'your_container_name'
    blob_path = 'your_blob_path'

    return AzureBlobStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        container_name,
        blob_path,
    )
{% endblock %}
