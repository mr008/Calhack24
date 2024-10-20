import base64
import requests
from io import BytesIO
from PIL import Image


def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string


# img = Image.open("path_to_your_image")
# base64_img = encode_image(img)

api = "https://api.hyperbolic.xyz/v1/chat/completions"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb25ub3JjYXJleTIwMDVAZ21haWwuY29tIiwiaWF0IjoxNzI5MzE2ODIyfQ.zPsooFImxwfpq5yjD5L5pyed32S9veO02tDiSkRjtKU"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                },
            ],
        }
    ],
    "model": "meta-llama/Llama-3.2-90B-Vision-Instruct",
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
}

response = requests.post(api, headers=headers, json=payload)
print(response.json())
