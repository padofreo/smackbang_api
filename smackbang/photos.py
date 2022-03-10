import requests
from dotenv import load_dotenv, find_dotenv
import os

env_path = find_dotenv()
load_dotenv(env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


def get_photo(cities):
    urls = []
    for city in cities:
        #the response of this is a JSON file that generates a photo reference
        url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={city}&key={GOOGLE_API_KEY}&inputtype=textquery&fields=name,photos'
        response = requests.request("GET", url).json()
        #the reference that we need to get the photo
        photo_ref = response["candidates"][0]["photos"][0]["photo_reference"]
        #make another request for a photo response and return url list
        photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={GOOGLE_API_KEY}&maxwidth=400&maxheight=400'
        response_photo = requests.request("GET",photo_url).url
        urls.append(response_photo)
    return urls

if __name__ == "__main__":
    images = get_photo(["Bangkok","Singapore","Hanoi","Phuket"])
    for url in images:
        print(url)
