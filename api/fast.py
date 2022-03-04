from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from smackbang.matches import get_matches

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

@app.get("/matches")
def matches(origin_one='NRT', origin_two='SYD', departure_date='01/04/2022', continent='AS', return_date='', currency='USD'):

    matches_df = get_matches(origin_one, origin_two, departure_date, continent, return_date='', currency='USD')

    result = matches_df.to_dict(orient='split')

    return result
