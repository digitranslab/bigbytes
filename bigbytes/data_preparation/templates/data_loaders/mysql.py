{% extends "data_loaders/default.jinja" %}
{% block imports %}
from bigbytes.settings.repo import get_repo_path
from bigbytes.io.config import ConfigFileLoader
from bigbytes.io.mysql import MySQL
from os import path
{{ super() -}}
{% endblock %}


{% block content %}
@data_loader
def load_data_from_mysql(*args, **kwargs):
    """
    Template for loading data from a MySQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.bigbytes.ai/design/data-loading#mysql
    """
    query = 'Your MySQL query'  # Specify your SQL query here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with MySQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)
{% endblock %}
