import numpy as np
import pandas as pd
import requests
import os
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)
TEQUILA_API_KEY = os.getenv('TEQUILA_API_KEY')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_RAPIDAPI_KEY = os.getenv('X_RAPIDAPI_KEY')

def get_city_location(cities):
    city_url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/cities.json"
    headers = {
        'x-access-token': X_ACCESS_TOKEN,
        'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
        'x-rapidapi-key': X_RAPIDAPI_KEY
    }

    response = requests.request("GET", city_url, headers=headers).json()

    city_location = []

    for city in cities:
        df = pd.DataFrame.from_dict(response)[['code', 'coordinates']].dropna()
        city_location.append(df.loc[df['code'] == city].coordinates.apply(pd.Series))
    result = pd.concat(city_location)
    df = pd.DataFrame(cities)

    result["city_code"] = df.values
    result.reset_index(inplace = True)
    result.drop(columns="index", inplace =True)
    return result

if __name__ == '__main__':
    print(get_city_location(['SYD']))
