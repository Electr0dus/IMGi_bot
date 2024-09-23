import base64
import json
import time
import logging
import requests

import config


class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, style: str, images=1, width=1024, height=1024, negative=None, ):
        params = {
            "type": "GENERATE",
            "style": style,
            "numImages": images,
            "width": width,
            "height": height,
            "negativePromptUnclip": negative,
            "generateParams": {
                "query": f"{prompt}"
            }
        }
        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def generation_image(self, request_id, attemps=10, delay=10):
        while attemps > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attemps -= 1
            time.sleep(delay)


api = Text2ImageAPI('https://api-key.fusionbrain.ai/', config.API_KANDINSKY, config.SECRET_KEY)


# Функция для генерации изображения по запросу пользователя
def generate_image(file_name_user: str, promt: str = 'Кот', width: str = 1024, height: str = 1024,
                   negative: str = None, style: str = 'string'):
    model_id = api.get_model()
    uuid = api.generate(prompt=promt, model=model_id, width=width, height=height, negative=negative, style=style)
    images = api.generation_image(uuid)
    convert_images(images, file_name=file_name_user)


# Конвертировать набор байтов в картинку PNG
def convert_images(images, file_name: str):
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    final_path = 'generic_photo_user/' + file_name
    logging.info(f'Successfully generate {file_name}')
    with open(final_path, 'wb') as file:
        file.write(image_data)




generate_image('my_image1.png', 'мотоцикл', style='ANIME')
