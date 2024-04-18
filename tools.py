import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats


def filter_outliers(series: pd.Series, max_z_score=3, interpolation='linear'):
    X = series.index.to_numpy().astype('float')
    Y = series.values
    C = np.polyfit(X, Y, 1)
    trend = np.polyval(C, X)
    diff = (Y - trend)**2

    z_score = stats.zscore(diff)
    series = series.copy()
    series[z_score > max_z_score] = pd.NA
    series = series.interpolate(method=interpolation)
    return series, trend


def offset_features_extractor(offsets):
    def extractor(series, last_n=None):
        lo = -min(np.array(offsets).flatten().min(), 0)
        hi = max(np.array(offsets).flatten().max(), len(series))

        start = len(series) - last_n if last_n else lo

        features = []
        for item in offsets:
            item_features = np.array([series.to_numpy()[[i + j for j in item]] for i in range(start, hi)])
            item_features = np.sum(item_features, axis=-1)
            features.append(item_features)

        features = np.stack(features, axis=-1)
        Y = series.to_numpy()[lo:]
        if last_n:
            Y = series[-last_n:]

        return features, Y

    return extractor


def linreg_prediction(series, feature_extractor, periods=4):
    total = len(series)
    last_period = series.tail(1).idxmax()

    series = series.copy()
    X, Y = feature_extractor(series)
    reg = LinearRegression().fit(X, Y)

    for i in range(periods):
        X2, _ = feature_extractor(series, 1)
        next_week = reg.predict(X2[-1:])

        last_period += 1
        series = pd.concat([series, pd.Series(next_week, index=[last_period])])

    return series[total-1:]


def build_coexistence_matrix(items: list, source: pd.DataFrame, group_column: str, match_column: str):
    N = len(items)
    mat = np.zeros([N, N])
    pairs = source.merge(source, on=group_column, suffixes=('_1', '_2'))

    for i in range(N):
        for j in range(i + 1, N):
            item1 = items[i]
            item2 = items[j]

            total = len(source[source[match_column] == item1])
            total_with_j = len(pairs[(pairs[match_column+'_1'] == item1) & (pairs[match_column+'_2'] == item2)].count())

            mat[i, j] = total_with_j / total
            mat[j, i] = total_with_j / total

    return mat
