import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import base64
from django.utils import timezone
from dotenv import load_dotenv
from io import BytesIO
from django.core.files.base import ContentFile
from apps.core.models import GeneratedImage, User
import uuid
import requests
from PIL import Image

load_dotenv()

class DallEChat(WebsocketConsumer):
    def connect(self):
        print('Conectandose al websocket...')
        
        self.user_id = self.scope['user'].id
        self.room_name = f'session_{self.user_id}'
        print('Asignando conexión en la sala: {}'.format(self.room_name))
        
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()
        
        print("Conexion aceptada para el usuario con ID {} en la sala: {} ".format(self.user_id, self.room_name))

    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        print(f'Conexión finalizada para el usuario con ID {self.user_id}')
        return super().disconnect(code)

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            img64 = text_data_json['img64']
            sender_id = self.scope['user'].id

            async_to_sync(self.channel_layer.group_send)(self.room_name, {
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

    def chat_message(self, event):
        
        message = event['message']
        datetime = event['datetime']
        sender_id = event['sender_id']
        img64 = event['img64']
        current_user_id= self.scope['user'].id
        
        response, condition = self.dalle_response(message, img64, int(sender_id))
        
        if sender_id == current_user_id:
            
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'success': condition,
                'message': message,
                'img': response,
                'datetime': datetime
            }))
            
            print("Mensaje enviado")
        
    def dalle_response(self, message, img64, id):
        try:            
        
            user = User.objects.get(id=id)
                
            decoded = base64.b64decode(img64) 
            image_io = BytesIO(decoded)
            
            with Image.open(image_io) as img:
                img = img.convert('RGBA')
                img_io = BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                image_data = img_io.getvalue()    
                     
            response = requests.post(
            "https://api.deepai.org/api/image-editor",
            files=
            {
                'image': image_data,
                'text': str(message),
                
            },
            
            headers={'api-key': '813cf899-d542-4f56-b4a0-2a17eeb88c57'}
            
            )
            
            if response.status_code != 200:
                print("Error al consultar con la API de DeepAI: ", response.text)
                return None, False
            
            response = response.json()
            output_url = response['output_url']
            deep_image = requests.get(output_url)
            
            if deep_image.status_code != 200:
                print("Error al recibir la imagén generada: ", deep_image.text)
                return None, False
            
            with Image.open(BytesIO(deep_image.content)) as new_img:
                new_img_io = BytesIO()
                new_img.save(new_img_io, format='PNG')
                new_img_io.seek(0)
                new_image_data = new_img_io.getvalue() 
   
            filename = 'image_{}.png'.format(str(uuid.uuid4()))
            image_model = GeneratedImage()
            image_model.user = user
            image_model.Img.save(name=filename, content=ContentFile(new_image_data, name=filename)) 
            image_model.save()
            img_url = image_model.Img.url
            
            return img_url, True
            
        except Exception as e:
            print(f"Error al generar/guardar la imagen: {e}")
            return None, False