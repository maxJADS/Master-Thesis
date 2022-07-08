"""
This is a boilerplate pipeline 'spectral_analysis'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import compute_spectrogram, octave_intensities, entropy_spectrum, PCA_intensities

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=compute_spectrogram,
            inputs=["data_filtered", "params:N"],
            outputs=["df_f", "df_t", "df_Sxx"],
            name="spectral_spectrogram_node",
        ),
        node(
            func=octave_intensities,
            inputs=["df_f", "df_t", "df_Sxx", "params:N"],
            outputs=["df_intensities", "df_intensities_rel", "df_lines"],
            name="spectral_octave_node",
        ),
        node(
            func=entropy_spectrum,
            inputs=["df_intensities", "params:N"],
            outputs="df_KL",
            name="spectral_entropy_node",
        ),
        node(
            func=PCA_intensities,
            inputs="df_intensities",
            outputs="df_components",
            name="spectral_PCA_node",
        ),
    ])
