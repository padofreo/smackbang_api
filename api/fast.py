from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from smackbang.matches import get_matches
from smackbang.twitter import analyze_tweet
from smackbang.locations import get_city_location
from smackbang.photos import get_photo
from smackbang.preprocess import DateFormatter, DateEncoder, TimeFeaturesEncoder, haversine_vectorized, DistanceTransformer, duration_process, set_preproc_pipeline
from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import multipart
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import set_config
import joblib
import xgboost

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Welcome to smackbang, the place to find the best middle ground to meet friends, family, colleagues"}

@app.get("/locations")
def city_locations(cities='SIN,KUL,NYC'):
    cities_list = cities.split(',')
    df = get_city_location(cities_list)
    result = df.to_dict(orient='dict')
    return result

@app.get("/matches")
def matches(origin_one='NRT', origin_two='SYD', departure_date='01/04/2022', continent='AS', return_date='', currency='USD'):
    matches_df = get_matches(origin_one, origin_two, departure_date, continent, return_date, currency)
    matches_df.columns = ['_'.join(col) for col in matches_df.columns.values]
    result  = matches_df.to_dict(orient='dict')
    return result

@app.get("/twitter")
def twitter(keywords='Bangkok,New Zealand,Russia,Dhaka'):
    keywords_list = keywords.lower().split(",")
    df = analyze_tweet(keywords_list)
    result  = df.to_dict()
    return result

@app.get("/photos")
def twitter(cities='Bangkok,New Zealand,Russia,Dhaka'):
    urls = []
    for city in cities:
        #the response of this is a JSON file that generates a photo reference
        api_key = "AIzaSyCMMb6QvT3xndUa0Phh5o2S2NWhmAKa5-A"
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={city}&key={api_key}&inputtype=textquery&fields=name,photos'
        response = requests.request("GET", url).json()
        #the reference that we need to get the photo
        photo_ref = response["candidates"][0]["photos"][0]["photo_reference"]
        #make another request for a photo response and return url list
        photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={api_key}&maxwidth=400&maxheight=400'
        response_photo = requests.request("GET",photo_url).url
        urls.append(response_photo)

    return {'images':[urls]}

@app.post("/predict")
def upload_file(file: UploadFile = File(...)):
    X = pd.read_csv(file.file)
    model = joblib.load('../model.joblib')
    preds = model.predict(X)
    return {'preds': [float(pred) for pred in preds]}
