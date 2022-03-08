## preprocessing.py imports
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn import set_config
import joblib

#custom
from smackbang.preprocess import DateFormatter, DateEncoder, TimeFeaturesEncoder, haversine_vectorized, DistanceTransformer, duration_process, set_preproc_pipeline

# implement train() function
def train(X_train, y_train, pipeline):
    '''returns a trained pipelined model'''
    pipeline.fit(X_train, y_train)
    return pipeline

def compute_mae(y_pred, y_true):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))

# implement evaluate() function
def evaluate(X_test, y_test, pipeline):
    '''returns the value of the RMSE'''
    response=[]
    y_pred = pipeline.predict(X_test)
    mae = compute_mae(y_pred, y_test)
    return mae

if __name__ == '__main__':
    df = pd.read_csv('../data/train_data.csv')
    # set X and y
    y = df["Price"]
    X = df.drop("Price", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # Instantiate preprocessing pipeline
    preproc_pipeline = set_preproc_pipeline()
    final_pipe = Pipeline([('preproc', preproc_pipeline),
                           ('xgb_reg_model',
                            XGBRegressor(eta=0.08,
                                         max_depth=12,
                                         n_estimators=100))])
    # train the pipeline
    trained_model = train(X_train, y_train, final_pipe)
    # evaluate the pipeline
    mae = evaluate(X_test, y_test, final_pipe)

    joblib.dump(trained_model, '../model.joblib')
