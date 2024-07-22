import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from openai import OpenAI
import base64
from django.utils import timezone
import os
from dotenv import load_dotenv
from pathlib import Path
from io import BytesIO
from django.core.files.base import ContentFile
from apps.core.models import ImageDallE
import uuid
from PIL import Image

load_dotenv()

class DallEChat(WebsocketConsumer):
    def connect(self):
        
        print('Conectandose al websocket...')
        
        self.user_id = self.scope['user'].id
        print("id:", self.user_id)
        self.room_name = f'session_{self.user_id}'
        
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        
        self.accept()
        print("Conexion aceptada para el usuario con ID: ", self.user_id)

    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        print('Conexión finalizada')
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
            
            print("Procesando mensaje")
            
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")

    def chat_message(self, event):
        message = event['message']
        datetime = event['datetime']
        sender_id = event['sender_id']
        img64 = event['img64']
        current_user_id= self.scope['user'].id
        
        print("Enviando datos..")
        print(message)
        response = self.dalle_response(message)
        
        
        if sender_id == current_user_id:
            
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'img': response,
                'datetime': datetime
            }))
            
            print("Mensaje enviado")
        
    
    def dalle_response(self, message):
        try:            
            print(message)
            
            # decoded = base64.b64decode(img64) 
              
            # No decodificar por el momento
              
            # image_io = BytesIO(decoded)
            
            # with Image.open(image_io) as img:
            #     img = img.convert('RGBA')
            #     img_io = BytesIO()
            #     img.save(img_io, format='PNG')
            #     img_io.seek(0)
            #     image_data = img_io.getvalue()    
                
            #     if len(image_data) > 4 * 1024 * 1024:
            #         print('La imagen debe ser menor a 4 MB.')   
                            
            key = os.getenv("API_KEY")
            
            client = OpenAI(api_key= key)
            
            response = client.images.generate(
            # image= image_data,
            prompt= str(message),
            model="dall-e-3",
            quality= 'standard',
            n= 1,
            response_format= 'url',
            size= "1024x1024"
            )
            
            print(response)
            
            dalle_img = response.data[0].url
            
            print(dalle_img)
            
            # Aquí habria que editar luego, la imagen se tiene que descargar desde la URL con el paquete de requests
            
            # dalle_decoded = base64.b64decode(dalle64) 
            
            # filename = 'image_{}'.format(str(uuid.uuid4()))
            
            # image_model = ImageDallE()
                
            # image_model.Img.save(filename, ContentFile(dalle_decoded))   
            
            # image_model.Type = dalle_decoded
            
            # image_model.save()
            
            return dalle_img
            
        except Exception as e:
            print(f"Error al generar la imagen con DALL-E: {e}")
            return None
            