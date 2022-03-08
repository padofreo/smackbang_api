import requests
import shutil

def get_photo(city):
    #the response of this is a JSON file that generates a photo reference
    api_key = "AIzaSyD5pwvqobmq3KCcl2jJ0B2gf0Yci_EScyw"
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={city}&key={api_key}&inputtype=textquery&fields=name,photos'
    response = requests.request("GET", url).json()

    #the reference that we need to get the photo
    photo_ref = response["candidates"][0]["photos"][0]["photo_reference"]

    #make another request for a photo response
    photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={api_key}&maxwidth=400&maxheight=400'
    response_photo = requests.request("GET",photo_url, stream=True)

    #save it
    if response_photo.status_code == 200:
        with open(f'{city}.png', 'wb') as f:
            response_photo.raw.decode_content = True
            shutil.copyfileobj(response_photo.raw, f)
