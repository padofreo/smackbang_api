from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from smackbang.matches import get_matches
from smackbang.twitter import analyze_tweet
from smackbang.locations import get_city_location
from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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

@app.get("/predict")
def predict(df): #input params from matches_df
    # todo find out the input params for the endpoint
    # what data and columns types is the model.joblib expecting
    # do any preprocessing
    # create the dataframe to pass to model.joblib




    my_dict = dict(Airline=[Airline],
             source = [origin],
             destination= [city_to],
             origin_lon = [],
             origin_lat = [],
             destination_lon = [],
             destination_lat = [],
             departure_time = [formated_departure_local],
             arrival_time = [formatted_arrival_local],
             duration = [formatted_duration])

    X_pred = pd.DataFrame(my_dict)

    pipeline = joblib.load('model.joblib')

    result = pipeline.predict(X_pred)[0]

    return {
        "fare": result
