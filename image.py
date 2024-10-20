import base64
import requests
from io import BytesIO
from PIL import Image
import os
import chromadb

def encode_image(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string

# Path to the clothes folder
folder_path = "./clothes/"

# API information
api = "https://api.hyperbolic.xyz/v1/chat/completions"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ3c29uZzkwMDBAZ21haWwuY29tIiwiaWF0IjoxNzI5Mzg4ODQ1fQ.sKvYYt5hqY6Uoqf_imbWWxeXSpGcEgDTON3BKY7r9g0"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


#chromadb setup
client = chromadb.Client()
collection = client.get_or_create_collection('fruit')

# Function to process and send the image to the API
def process_image(image_path,image_id):
    try:
        img = Image.open(image_path)
        base64_img = encode_image(img)
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is this wardrobe item? Give me description of itself, its style and how can you pair it. Ignore the background and other irrelevant information. Limit the word to 50 words and make sure the descriptions are in a single not segemented text paragraph."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                        },
                    ],
                }
            ],
            "model": "meta-llama/Llama-3.2-90B-Vision-Instruct",
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
        }
        response = requests.post(api, headers=headers, json=payload)

        # Print the response
        if response.status_code == 200:
            result = response.json()
            description = result["choices"][0]["message"]["content"]
            print(description)
            collection.add(
                ids=[image_id],
                documents=[description]
            )
        else:
            print(f"Error processing {image_path}: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error opening or processing {image_path}: {str(e)}")

# Iterate over all files in the clothes folder

for index, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter image files
        image_path = os.path.join(folder_path, filename)
        process_image(image_path,str(index))

print(collection.query(query_texts='bright color', n_results=1))
'''
image_path = "./clothes/aoedaohdeaoeu.jpg"
process_image(image_path)
'''
