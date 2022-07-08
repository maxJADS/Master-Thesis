"""
This is a boilerplate pipeline 'evaluation'
generated using Kedro 0.18.0
"""

import numpy as np

def warning_additive(df, name, period, l, h, k):
    """computes warnings based on threshold values
    computed with percentile values calculated over a specified period and a factor k in an additive formula
    """

    warnings = list()
    skip = period
    values = list()
    calculate = 1
    for value in df[name]:
        if skip != 0:
            warnings.append(np.nan)
            values.append(value)
            skip -= 1
            continue
        elif skip == 0:
            calculate -= 1
            if calculate == 0:
                l_percentile = np.percentile(values, l)
                h_percentile = np.percentile(values, h)
                median = np.median(values)
                low = median + k * (l_percentile - median)
                high = median + k * (h_percentile - median)
            if value > high:
                warnings.append(1)
                skip = period
                calculate = 1
            elif value < low:
                warnings.append(-1)
                skip = period
                calculate = 1
            else:
                warnings.append(0)

    return warnings


def warning_multiplicative(df, name, period, l, h, k):
    """computes warnings based on threshold values
    computed with percentile values calculated over a specified period and a factor k in a multiplicative formula
    """

    warnings = list()
    skip = period
    values = list()
    calculate = 1
    for value in df[name]:
        if skip != 0:
            warnings.append(np.nan)
            values.append(value)
            skip -= 1
            continue
        elif skip == 0:
            calculate -= 1
            if calculate == 0:
                l_percentile = np.percentile(values, l)
                h_percentile = np.percentile(values, h)
                median = np.median(values)  # kan weg
                low = (l_percentile / median) / k * median
                high = (h_percentile / median) * k * median
            if value > high:
                warnings.append(1)
                skip = period
                calculate = 1
            elif value < low:
                warnings.append(-1)
                skip = period
                calculate = 1
            else:
                warnings.append(0)

    return warnings


def evaluation(df, dfmm, dfc, dfl, dfKL, dfpca, evaluation_params):
    """uses the additive and multiplicative warning functions to copmute warnings for all performance indicators"""

    l = evaluation_params['percentile_lower']
    h = evaluation_params['percentile_upper']
    k_list = evaluation_params['k_list']

    df['warnings_temp'] = warning_additive(df=df, name='Temp', period=12 * 24 * 31, l=l, h=h, k=k_list[0])

    ts = ' Temp'
    for column in ['min', 'max']:
        dfmm['warnings_{}'.format(column)] = warning_additive(df=dfmm, name=column + ts, period=12 * 24 * 31, l=l, h=h,
                                                              k=k_list[1])
    for column in ['std']:
        dfmm['warnings_{}'.format(column)] = warning_multiplicative(df=dfmm, name=column + ts, period=12 * 24 * 31, l=l,
                                                                    h=h, k=k_list[3])

    dfc['warnings_avg'] = warning_additive(df=dfc, name='gauss_1day', period=12 * 24 * 31, l=l, h=h, k=k_list[2])

    dfl.columns = dfl.columns.astype(int)
    for column in dfl:
        dfl['warnings_oct{}'.format(column)] = warning_multiplicative(df=dfl, name=column, period=31, l=l, h=h,
                                                                      k=k_list[4])
    dfl.columns = dfl.columns.astype(str)

    dfKL.columns = dfKL.columns.astype(int)
    dfKL['warnings_IG'] = warning_multiplicative(df=dfKL, name=1, period=31, l=l, h=h, k=k_list[5])
    dfKL.columns = dfKL.columns.astype(str)

    dfpca.columns = dfpca.columns.astype(int)
    for column in dfpca:
        dfpca['warnings_PC{}'.format(column)] = warning_additive(df=dfpca, name=column, period=31, l=l, h=h,
                                                                 k=k_list[6])
    dfpca.columns = dfpca.columns.astype(str)

    return df, dfmm, dfc, dfl, dfKL, dfpca
