import base64
import requests
from io import BytesIO
from PIL import Image
import os
import chromadb
from pinscrape import pinscrape

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


# chromadb setup
client = chromadb.Client()
collection = client.get_or_create_collection('clothes')

# Function to process and send the image to the API
def process_image(image_path, image_id):
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
                            "text": "What is this wardrobe item? Give me description of itself, its style and how can you pair it. Ignore the background and other irrelevant information. Limit the word to 50 words and make sure the descriptions are in a single not segmented text paragraph."
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
            "temperature": 0.5,
            "top_p": 0.9,
        }
        response = requests.post(api, headers=headers, json=payload)

        # Print the response
        if response.status_code == 200:
            result = response.json()
            description = result["choices"][0]["message"]["content"]
            print("imageid: ", image_id, " : ", description)
            collection.add(
                ids=[image_id],
                documents=[description]
            )
        else:
            print(f"Error processing {image_path}: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error opening or processing {image_path}: {str(e)}")

# Function to process all images in the clothes folder
def process_all_images():
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):  # Filter image files
            image_path = os.path.join(folder_path, filename)
            process_image(image_path, filename)

# Function to query based on user input
def query_collection(userinput):
    print("User input:", userinput)
    results = collection.query(query_texts=[userinput], n_results=2)
    print("Query Results:", results)

def output_image_description:
    # Function to process and send the image to the API
def process_image(image_path, image_id):
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
                            "text": "What is this wardrobe item? Give me description of itself, its style and how can you pair it. Ignore the background and other irrelevant information. Limit the word to 50 words and make sure the descriptions are in a single not segmented text paragraph."
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
            "temperature": 0.5,
            "top_p": 0.9,
        }
        response = requests.post(api, headers=headers, json=payload)

        # Print the response
        if response.status_code == 200:
            result = response.json()
            description = result["choices"][0]["message"]["content"]
            print("imageid: ", image_id, " : ", description)
        else:
            print(f"Error processing {image_path}: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error opening or processing {image_path}: {str(e)}")


# Main execution flow
if __name__ == "__main__":
    
    # Process all images in the folder and add to the collection
    process_all_images()

    # ADD AN ADDITIONAL IMAGE
    #file_name = os.path.basename(file_path)
    #process_image(file_path,file_name)

    while True:
        # Query the collection based on the user input
        userinput = input("Enter your search query (e.g., 'gothic style'): ")
        query_collection(userinput)

        # The scraper function that fetches the Pinterest photos
        details = pinscrape.scraper.scrape(userinput, "./psoutput", {}, 5, 20)
        if details["isDownloaded"]:
            print("\nDownloading completed !!")
            print(f"\nTotal URLs found: {len(details['extracted_urls'])}")
            print(f"\nTotal images downloaded (including duplicate images): {len(details['urls_list'])}")
        else:
            print("\nNothing to download !!", details)