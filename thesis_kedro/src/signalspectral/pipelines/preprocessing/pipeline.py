"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import minmaxstd, convolutions, filter_outliers

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=minmaxstd,
                inputs=["data_G", "params:N"],
                outputs=["data_G_loaded", "data_minmaxstd"],
                name="preprocessing_minmaxstd_node",
            ),
            node(
                func=convolutions,
                inputs="data_minmaxstd",
                outputs="data_convolutions",
                name="preprocessing_convolutions_node",
            ),
            node(
                func=filter_outliers,
                inputs=["data_convolutions", "params:percentile_params"],
                outputs="data_filtered",
                name="preprocessing_filter_node",
            ),
        ]

    )
