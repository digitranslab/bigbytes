def get_source_name(dbt_project_name: str) -> str:
    return f'bigbytes_{dbt_project_name}'


def get_source_table_name_for_block(block) -> str:
    return f'{block.pipeline.uuid}_{block.uuid}'