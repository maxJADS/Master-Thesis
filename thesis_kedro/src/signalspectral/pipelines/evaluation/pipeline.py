"""
This is a boilerplate pipeline 'evaluation'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluation

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
        node(
            func=evaluation,
            inputs=["data_G_loaded", "data_minmaxstd", "data_convolutions", "df_lines", "df_KL", "df_components", "params:evaluation_params"],
            outputs=["df_G_evaluated", "df_minmaxstd_evaluated", "df_average_evaluated", "df_lines_evaluated", "df_KL_evaluated", "df_components_evaluated"],
            name="evaluation_node",
        ),
    ]
    )
