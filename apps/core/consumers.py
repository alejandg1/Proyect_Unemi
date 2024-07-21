import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from openai import OpenAI
import base64
import requests
from io import BytesIO
from django.utils import timezone

class DallEChat(WebsocketConsumer):
    def connect(self):
        
        print('Conexión con websocket')
        
        self.user_id = self.scope['user'].id
        print("id:", self.user_id)
        self.room_name = f'session_{self.user_id}'
        
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        
        self.accept()
        print("Conexion aceptada")

    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        print('Conexión finalizada')
        return super().disconnect(code)

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print(text_data)
            message = text_data_json['message']
            print("Mensaje:", message)
            sender_id = self.scope['user'].id

            async_to_sync(self.channel_layer.group_send)(self.room_name, {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
            })
            
            print("Procesando mensaje")
            
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")

    def chat_message(self, event):
        message = event['message']
        datetime = event['datetime']
        sender_id = event['sender_id']
        current_user_id= self.scope['user'].id
        print("Enviando mensaje: ", message)
        response = '/media/images/CRUZ-RUIZ-VICTOR-HUGO-scaled.jpg'
        
        if sender_id == current_user_id:
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'image': response,
                'datetime': datetime
            }))
            print("Mensaje enviado")
        
    
    # def dalle_response(self, message):
    #     try:            
    #         client = OpenAI()
    #         response = client.images.edit(
    #         model="dall-e-3",
    #         prompt="a white siamese cat",
    #         size="1024x1024",
    #         quality="standard",
    #         n=1,
    #         )

    #         image_url = response['data'][0]['url']

    #         image_response = requests.get(image_url)
            
    #         if image_response.status_code == 200:
    #             image_data = image_response.content
    #             image_base64 = base64.b64encode(image_data).decode('utf-8')
    #             print(image_base64)
    #             return image_base64
                
    #         else:
                
    #             return None
            
    #     except Exception as e:
    #         print(f"Error al generar la imagen con DALL-E: {e}")
    #         return None
            