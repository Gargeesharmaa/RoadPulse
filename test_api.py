import requests
from PIL import Image
import io

# 1. Update the URL to match your server configuration
url = "http://127.0.0.1:8000/reports/"  

# 2. Create a small, valid blank JPEG image in memory so PIL doesn't crash
img = Image.new('RGB', (100, 100), color = 'red')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='JPEG')
img_byte_arr.seek(0)

files = {
    "image": ("pothole.jpg", img_byte_arr, "image/jpeg")
}

data = {
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "address": "1024 Maple Avenue, near downtown intersection",
    "description": "Deep pothole in the middle lane causing cars to swerve dangerously."
}

print("Sending request with valid image bytes...")
response = requests.post(url, files=files, data=data)

print(f"Status Code: {response.status_code}")
print("Response text:")
print(response.text)