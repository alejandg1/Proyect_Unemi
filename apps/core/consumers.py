import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
from django.utils import timezone
from io import BytesIO
from django.core.files.base import ContentFile
from apps.core.models import GeneratedImage, User
import uuid
import aiohttp
from PIL import Image
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
load_dotenv()


def save_image_sync(user, image_data, filename):
    image_model = GeneratedImage()
    image_model.user = user
    image_model.Img.save(
        name=filename, content=ContentFile(image_data, name=filename))
    image_model.save()
    return image_model.Img.url


class DallEChat(AsyncWebsocketConsumer):
    async def connect(self):
        print('Conectandose al websocket...')

        self.user_id = self.scope['user'].id
        self.room_name = f'session_{self.user_id}'
        print(f'Asignando conexión en la sala: {self.room_name}')

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        print(f"Conexión aceptada para el usuario con ID {
              self.user_id} en la sala: {self.room_name}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print(f'Conexión finalizada para el usuario con ID {self.user_id}')
        return await super().disconnect(code)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            img64 = text_data_json['img64']
            sender_id = self.scope['user'].id

            await self.channel_layer.group_send(self.room_name, {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'img64': img64.split(',')[1],
                'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
            })

        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    async def chat_message(self, event):
        message = event['message']
        datetime = event['datetime']
        sender_id = event['sender_id']
        img64 = event['img64']
        current_user_id = self.scope['user'].id

        response, condition = await self.dalle_response(message, img64, int(sender_id))

        if sender_id == current_user_id:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'success': condition,
                'message': message,
                'img': response,
                'datetime': datetime
            }))
            print("Mensaje enviado")

    async def dalle_response(self, message, img64, user_id):
        try:

            user = await sync_to_async(User.objects.get)(id=user_id)

            decoded = base64.b64decode(img64)
            image_io = BytesIO(decoded)

            with Image.open(image_io) as img:
                img = img.convert('RGBA')
                img_io = BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                image_data = img_io.getvalue()

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepai.org/api/image-editor",
                    data={
                        'image': image_data,
                        'text': str(message),
                    },
                    # headers={'api-key':
                    # '813cf899-d542-4f56-b4a0-2a17eeb88c57'}
                    headers={'api-key': os.getenv('DEEP_KEY')}
                ) as response:
                    if response.status != 200:
                        print(f"Error al consultar con la API de DeepAI: {await response.text()}")
                        return None, False

                    response_data = await response.json()
                    output_url = response_data['output_url']

                async with session.get(output_url) as deep_image:
                    if deep_image.status != 200:
                        print(f"Error al recibir la imagen generada: {await deep_image.text()}")
                        return None, False

                    new_image_data = await deep_image.read()

            filename = f'image_{uuid.uuid4()}.png'

            img_url = await sync_to_async(save_image_sync)(user, new_image_data, filename)

            return img_url, True

        except Exception as e:
            print(f"Error al generar/guardar la imagen: {e}")
            return None, False
