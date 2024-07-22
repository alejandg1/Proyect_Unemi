import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

base = Path(__file__).resolve().parent.parent
output = (os.path.join(base, 'media', 'images', 'dalle'))
key = os.getenv("API_KEY")
print(key)