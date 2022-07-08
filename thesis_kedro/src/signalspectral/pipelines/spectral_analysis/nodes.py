"""
This is a boilerplate pipeline 'spectral_analysis'
generated using Kedro 0.18.0
"""

import scipy
import pandas as pd
import math
import numpy as np
from sklearn.decomposition import PCA

def compute_spectrogram(data_filtered:pd.DataFrame, N:int):
    """computes the spectrogram of the temperature signal"""

    f, t, Sxx = scipy.signal.spectrogram(data_filtered['Temp - avg'], fs=1 / 300, nperseg=N)

    df_f = pd.DataFrame(f, columns=['f'])
    df_t = pd.DataFrame(t, columns=['t'])
    df_Sxx = pd.DataFrame(Sxx)
    df_Sxx.columns = df_Sxx.columns.astype(str)

    return df_f, df_t, df_Sxx


def octave_intensities(df_f, df_t, df_Sxx, N):
    """computes the absolute and relative octave intensities based on the spectrogram"""

    f = df_f.T.to_numpy()[0]
    t = df_t.T.to_numpy()[0]
    Sxx = df_Sxx.to_numpy()

    delta_t = 5 * 60
    T = N * delta_t
    delta_f = 1 / T
    F = N * delta_f / 2
    M = int(round(np.log(F / delta_f)))

    parts = M
    borders = [(delta_f * math.exp((i / M) * np.log(F / delta_f))) for i in range(M + 1)]
    indi = [len(f[f <= borders[i]]) for i in range(len(borders))]
    metrics_relative = dict()
    metrics = dict()
    for d in range(len(t)):
        # tindex = t[d]
        F = [Sxx[i][d] for i in range(len(Sxx))]
        metrics[t[d]] = dict()
        metrics_relative[t[d]] = dict()
        sumf = sum(F[:])
        for b in range(1, parts + 1):
            metrics_relative[t[d]][b] = sum(F[indi[b - 1]:indi[b]]) / sumf
            metrics[t[d]][b] = sum(F[indi[b - 1]:indi[b]])

    df_intensities = pd.DataFrame(metrics)
    df_intensities.columns = df_intensities.columns.astype(str)
    df_intensities_rel = pd.DataFrame(metrics_relative)
    df_intensities_rel.columns = df_intensities_rel.columns.astype(str)

    lines = dict()
    for i in range(1, 5 + 1):
        line = list()
        for m in metrics:
            line.append(metrics[m][i])
        lines[i] = line

    df_lines = pd.DataFrame(lines)
    df_lines.columns = df_lines.columns.astype(str)

    return df_intensities, df_intensities_rel, df_lines


def entropy_spectrum(df_intensities, N):
    """computes the entropy/Kullback-Leibner divergence/information gain based on the octave intensities"""

    df_intensities.columns = df_intensities.columns.astype(float)
    intensities = df_intensities.to_dict()

    delta_t = 5 * 60
    T = N * delta_t
    delta_f = 1 / T
    F = N * delta_f / 2
    M = int(round(np.log(F / delta_f)))

    Poct = intensities
    Qpinkyoct = 1 / M
    KL = dict()
    for i in Poct:
        KL[i] = sum([Poct[i][j] / Qpinkyoct for j in range(1, M + 1)])

    df_KL = pd.DataFrame(zip(*KL.items())).T
    df_KL.columns = df_KL.columns.astype(str)

    return df_KL


def PCA_intensities(df_intensities):
    """computes the first two principal components of the octave intensities"""

    df_intensities.columns = df_intensities.columns.astype(float)
    metrics = df_intensities.to_dict()
    df_metrics = pd.DataFrame(metrics).T

    df = df_metrics.rename({1: 'octave 1',
                            2: 'octave 2',
                            3: 'octave 3',
                            4: 'octave 4',
                            5: 'octave 5'}, axis=1)
    features = df.columns

    pca = PCA(2)
    components = pca.fit_transform(df[features])
    labels = {str(i): f"PC {i + 1} ({var:.1f}%)" for i, var in enumerate(pca.explained_variance_ratio_ * 100)}

    df_components = pd.DataFrame(components)
    df_components.columns = df_components.columns.astype(str)

    return df_components