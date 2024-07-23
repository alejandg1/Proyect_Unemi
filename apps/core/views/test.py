import requests
from PIL import Image
from io import BytesIO

url = 'https://api.deepai.org/job-view-file/f576ae8b-2857-4964-bb97-c6d34bc5e572/outputs/output.jpg'
save_path = 'media/payaso.jpg'
response = requests.get(url)

if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(save_path)
        print(f'Imagen guardada en {save_path}')