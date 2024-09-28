import asyncio
import base64
import json
import logging
import os

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

    async def generation_image(self, request_id, attemps=20, delay=10):
        while attemps > 0:
            logging.info(f'There are still requests left - {attemps}')
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attemps -= 1
            await asyncio.sleep(delay)


api = Text2ImageAPI('https://api-key.fusionbrain.ai/', config.API_KANDINSKY, config.SECRET_KEY)


# Функция для генерации изображения по запросу пользователя
async def generate_image(file_name: str, dir_name: str, prompt: str = 'Кот', width: str = 1024, height: str = 1024,
                         negative: str = None, style: str = 'string'):
    model_id = api.get_model()
    logging.info('START generation image')
    uuid = api.generate(prompt=prompt, model=model_id, width=width, height=height, negative=negative, style=style)
    images = await api.generation_image(uuid)
    convert_images(images, dir_name, file_name)


# Конвертировать набор байтов в картинку PNG
def convert_images(images, dir_name: str, file_name: str):
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    final_path = f'generic_photo_user/{dir_name}/{file_name}'
    logging.info(f'Successfully generate {final_path}')
    with open(final_path, 'wb') as file:
        file.write(image_data)


# Функция для сохранения сгенерированной фотографии под названием пользователя
def save_image_user(name_file: str):
    pass


# Функция для проверки правильности написания формы файла, если верно вернёт - True, иначе - False
def check_name_file(file_name: str):
    for file in file_name:
        if file == " ":
            return False
    new_name_file = file_name.split('.')
    if len(new_name_file) > 1:
        if new_name_file[1] == 'png':
            return True
        else:
            return False
    else:
        return False


# Функция для создания директории пользователя, где они будут хранить свои фото
def make_dir_user(name_dir: str):
    # если папка ещё не создана, создать её
    if not os.path.isdir(f'generic_photo_user/{name_dir}'):
        os.mkdir(f'generic_photo_user/{name_dir}')


# Функция удаления фото
def delete_img(dir_name: str, name_file: str):
    logging.info(f'The image was deleted successfully {name_file}')
    path_base = os.getcwd()
    # Перейти в нужную директорию для удаления фото
    os.chdir(f'generic_photo_user/{dir_name}')
    os.remove(name_file)
    # Вернуться в рабочую директрию обратно
    os.chdir(path_base) # ЗДЕСЬ ОШИБКА!!!!

