# ---------------------------
#     Data Preprocessing
# ---------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def data_dropna(df):
    """
        dropping duplicates
    """
    df = df.dropna(inplace=True)
    return df


def data_drop_dup(df):
    """
        drop nan values.
    """
    df = df.drop_duplicates(inplace=True)
    return df


class DateFormatter(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        # stateless transformer
        return self

    def transform(self, X):
        # assumes X is a DataFrame
        Xdate = X.apply(pd.to_datetime)
        return Xdate

class DateEncoder(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        new_cols = []
        for col in X_copy.columns:
            new_cols.append(X_copy[col].dt.month)
            new_cols.append(X_copy[col].dt.day)
        return pd.concat(new_cols, axis=1)


class TimeFeaturesEncoder(BaseEstimator, TransformerMixin):
    """Extract the day of week (dow), the hour, the month and the year from a time column."""

    def __init__(self, time_zone_name='UTC'):
        #         self.time_column = time_column
        self.time_zone_name = time_zone_name

    def extract_time_features(self, X):
        timezone_name = self.time_zone_name
        #         time_column = self.time_column
        df = X.copy()
        #         df.index = df[time_column].apply(pd.to_datetime)
        old_cols = list(df.columns)
        for col in old_cols:
            df[col] = pd.to_datetime(df[col])
            df[col] = df[col].dt.tz_localize(timezone_name)
            df[f"{col}_hour"] = df[col].dt.hour
            df[f"{col}_minute"] = df[col].dt.minute
        df.drop(columns=old_cols, inplace=True)
        return df

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """Returns a copy of the DataFrame X with only four columns: 'hour', 'month'"""
        return self.extract_time_features(X)  #.reset_index(drop=True)


def haversine_vectorized(df,
                         start_lat="origin_one_latitude",
                         start_lon="origine_one_longitude",
                         end_lat="origin_two_latitude",
                         end_lon="origin_two_longitude"):
    """
        Calculates the great circle distance between two points
        on the earth (specified in decimal degrees).
        Vectorized version of the haversine distance for pandas df.
        Computes the distance in kms.
    """

    lat_1_rad, lon_1_rad = np.radians(df[start_lat].astype(float)), np.radians(
        df[start_lon].astype(float))
    lat_2_rad, lon_2_rad = np.radians(df[end_lat].astype(float)), np.radians(
        df[end_lon].astype(float))
    dlon = lon_2_rad - lon_1_rad
    dlat = lat_2_rad - lat_1_rad

    a = np.sin(dlat / 2.0)**2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(
        dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c


# create a DistanceTransformer
class DistanceTransformer(BaseEstimator, TransformerMixin):
    """
        Computes the haversine distance between two GPS points.
        Returns a copy of the DataFrame X with only one column: 'distance'.
    """

    def __init__(self,
                 start_lat="origin_one_latitude",
                 start_lon="origin_one_longitude",
                 end_lat="origin_two_latitude",
                 end_lon="origin_two_longitude"):
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X_ = X.copy()
        X_["distance"] = haversine_vectorized(X_,
                                              start_lat=self.start_lat,
                                              start_lon=self.start_lon,
                                              end_lat=self.end_lat,
                                              end_lon=self.end_lon)
        return X_[['distance']]


def duration_process(df):
    duration_obj = df.values.reshape(-1)
    print(duration_obj)
    col = 'duration'
    for i in range(len(duration_obj)):
        if len(duration_obj[i].split(' ')) == 2:
            pass
        else:
            if 'h' in duration_obj[i]:
                duration_obj[i] = duration_obj[i] + ' ' + '0m'
            else:
                duration_obj[i] = '0h' + ' ' + duration_obj[i]
    df = pd.DataFrame(duration_obj, dtype='str')
    df[f'{col}_hour'] = df[0].str.split("h ", n=1,
                                        expand=True)[0].astype('int64')
    df[f'{col}_min'] = df[0].str.split(
        " ", n=2, expand=True)[1].str.strip('m').astype('int64')
    df.drop(columns=0, inplace=True)
    return df


def set_preproc_pipeline():
    # create date pipeline
    date_pipe = Pipeline([('date_format', DateFormatter()),
                          ('date_enc', DateEncoder())])

    # create time pipeline
    time_pipe = Pipeline([('time_enc', TimeFeaturesEncoder()),
                          ('ohe',
                           OneHotEncoder(handle_unknown='ignore',
                                         sparse=False))])

    dist_pipe = Pipeline([('dist_trans', DistanceTransformer()),
                          ('stdscaler', StandardScaler())])

    duration_pipe = FunctionTransformer(duration_process)

    preproc_pipe = ColumnTransformer(
        [('date_pipe', date_pipe,
          ['Date_of_Journey', 'Dep_Time', 'Arrival_Time']),
         ('time_pipe', time_pipe, ['Dep_Time', 'Arrival_Time']),
         ('dist_pipe', dist_pipe, [
             "origin_one_latitude", "origin_one_longitude",
             "origin_two_latitude", "origin_two_longitude"
         ]), ('duration_pipe', duration_pipe, ['Duration'])],
        remainder='drop')
    final_pipe = Pipeline([('preproc', preproc_pipe),
                           ('stdscaler', StandardScaler())])

    # display time pipeline
    return final_pipe
