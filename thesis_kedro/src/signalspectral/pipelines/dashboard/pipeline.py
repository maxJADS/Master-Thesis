"""
This is a boilerplate pipeline 'dashboard'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_dashboard

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_dashboard,
                inputs=["data_G_loaded", "data_minmaxstd", "data_convolutions", "data_filtered",
                        "df_f", "df_t", "df_Sxx",
                        "df_lines", "df_KL", "df_components",
                        "df_G_evaluated", "df_minmaxstd_evaluated", "df_average_evaluated", "df_lines_evaluated", "df_KL_evaluated", "df_components_evaluated",
                        "params:name"],
                outputs=None,
                name="dashboard_node",
            ),
        ]
    )
