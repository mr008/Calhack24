import requests

url = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb25ub3JjYXJleTIwMDVAZ21haWwuY29tIiwiaWF0IjoxNzI5MzE2ODIyfQ.zPsooFImxwfpq5yjD5L5pyed32S9veO02tDiSkRjtKU"
}
data = {
    "messages": [
        {
            "role": "system",
            "content": "You are a customer service agent for a company named Spork. Handle all interactions professionally and in customer-service like manner. The company sells sporks and the customer can always find more information on the website \"www.sporks4us.com\". Always leave messages open for conversation or further questions. Keep your answers short and concise. If you do not know something for certain (like a listing on the website, material of sporks, etc etc) DO NOT say its available or that you know. DO NOT give advice or reccomendations for items you do not know exist on sporks4us.com. Do not make assumptions about product offerings."
        },
    ],
    "model": "meta-llama/Llama-3.2-3B-Instruct",
    "max_tokens": 4096,
    "temperature": 0.7,
    "top_p": 0.9
}
    
while True:
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    message = json["choices"][0]["message"]
    print(message["content"], end="\n\n")
    data["messages"].append(message)
    user_input = input("")
    data["messages"].append({"role": "user", "content": user_input})
    print()

