{% extends "data_loaders/default.jinja" %}
{% block imports %}
from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.redshift import Redshift
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_data_from_redshift(*args, **kwargs):
    """
    Template for loading data from a Redshift cluster.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.ai/design/data-loading#redshift
    """
    query = 'your_redshift_selection_query'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Redshift.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
{% endblock %}
