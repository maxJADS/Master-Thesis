"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""

import pandas as pd
import numpy as np
from scipy import signal

def minmaxstd(raw_data: pd.DataFrame, N) -> pd.DataFrame:
    """compute the minimum and maximum temperatures, and standard deviation
    with a rolling window of specified length"""
    data = raw_data

    data['max Temp'] = data['Temp'].rolling(N, min_periods=1).max()
    data['min Temp'] = data['Temp'].rolling(N, min_periods=1).min()
    data['std Temp'] = data['Temp'].rolling(N, min_periods=1).std()
    data['std Temp'][0] = 0

    data_minmax = data
    return raw_data, data_minmax


def convolutions(raw_data : pd.DataFrame) -> pd.DataFrame:
    """compute convolutions of the data on different timescales
    based on a Tukey window convolutions of lengths of a week/day/hour
    and detrend data by subtracting the 1week average from the temperature"""
    data = raw_data

    sig = data.Temp
    win_week = signal.windows.tukey(M=12 * 24 * 7, alpha=0.5, sym=False)
    data['gauss_1week'] = signal.convolve(sig, win_week, mode='same') / sum(win_week)
    win_day = signal.windows.tukey(M=12 * 24, alpha=0.5, sym=False)
    data['gauss_1day'] = signal.convolve(sig, win_day, mode='same') / sum(win_day)
    win_hour = signal.windows.tukey(M=12, alpha=0.5, sym=False)
    data['gauss_1hour'] = signal.convolve(sig, win_hour, mode='same') / sum(win_hour)

    data['Temp - avg'] = data['Temp'] - data['gauss_1week']

    data_convolutions = data
    return data_convolutions

def filter_outliers(data_convolutions: pd.DataFrame, percentiles):
    """filter outliers based on a lower and upper percentile of the 1hour convoluted data"""
    data = data_convolutions

    data = data[data['gauss_1hour'] < np.percentile(data['gauss_1hour'], percentiles['upper_percentile'])]
    data = data[data['gauss_1hour'] > np.percentile(data['gauss_1hour'], percentiles['lower_percentile'])]

    data_filtered = data
    return data_filtered


