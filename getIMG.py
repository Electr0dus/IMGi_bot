import requests
import config
URL = f'https://api-key.fusionbrain.ai/key/api/v1/text2image/run'

params = {
    "type": "GENERATE",
    "numImages": "1",
    "width": "1024",
    "height": "1024",
    "generateParams": {
        "query": f"Котики на мотоциклах"
    }
}


def get_image():
    # requ = requests.get()
    pass