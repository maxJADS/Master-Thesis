"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from signalspectral.pipelines import preprocessing as prep
from signalspectral.pipelines import spectral_analysis as span
from signalspectral.pipelines import evaluation as eval
from signalspectral.pipelines import dashboard as dash


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    preprocessing_pipeline = prep.create_pipeline()
    spectral_analysis_pipeline = span.create_pipeline()
    evaluation_pipeline = eval.create_pipeline()
    dashboard_pipeline = dash.create_pipeline()

    return {
        "__default__": preprocessing_pipeline + spectral_analysis_pipeline + evaluation_pipeline + dashboard_pipeline,
        "prep": preprocessing_pipeline,
        "span": spectral_analysis_pipeline,
        "eval": evaluation_pipeline,
        "dash": dashboard_pipeline
    }
