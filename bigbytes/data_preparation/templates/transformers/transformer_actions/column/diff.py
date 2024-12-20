{% extends "transformers/transformer_actions/action.jinja" %}
{% block action %}
    """
    Execute Transformer Action: ActionType.DIFF

    Calculates difference from previous row along column.

    Docs: https://docs.bigbytes.ai/guides/transformer-blocks#difference
    """
    action = build_transformer_action(
        df,
        action_type=ActionType.DIFF,
        arguments=[],  # Specify at most one column to compute difference with
        axis=Axis.COLUMN,
        outputs=[{'uuid': 'new_diff_column', 'column_type': 'number_with_decimals'}],
    )
{% endblock %}
