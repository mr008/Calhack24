import requests

url = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb25ub3JjYXJleTIwMDVAZ21haWwuY29tIiwiaWF0IjoxNzI5MzE2ODIyfQ.zPsooFImxwfpq5yjD5L5pyed32S9veO02tDiSkRjtKU"
}
data = {
    "messages": [
        {
            "role": "user",
            "content": "Ask me anything :)"
        },
        {
            "role": "assistant",
            "content": "If you could travel anywhere in the world right now, where would you go and why?"
        },
        {
            "role": "user",
            "content": "Interesting, I would go to Europe! Specifically Italy."
        },
        {
            "role": "assistant",
            "content": """Italy is a wonderful choice! The history, art, architecture, food, and culture are all so rich and vibrant. From the canals of Venice to the ancient ruins of Rome, and from the picturesque Tuscan countryside to the stunning Amalfi Coast, there's so much to explore.

If you could spend a day exploring Italy, what would be the top three places you would visit?"""
        }
    ],
    "model": "meta-llama/Llama-3.2-3B-Instruct",
    "max_tokens": 30000,
    "temperature": 0.7,
    "top_p": 0.9
}
  
response = requests.post(url, headers=headers, json=data)
response_json = response.json()
print(response_json["choices"][0]["message"])
# print(response.json())
