import requests
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
redirect_uri = os.getenv('REDIRECT_URI')

url = "https://getpocket.com/v3/oauth/request"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Accept": "application/json",
}
payload = {
    "consumer_key": consumer_key,
    "redirect_uri": redirect_uri,
}

response = requests.post(url, headers=headers, data=payload)

if response.status_code == 200:
    request_token = response.json()["code"]
    print(f"Request token: {request_token}")
else:
    print(f"Error obtaining request token: {response.text}")

print('Please authorize:')
print('https://getpocket.com/auth/authorize?request_token=' + request_token + '&redirect_uri=' + redirect_uri + '&consumer_key=' + consumer_key)

input("Press Enter to continue after authorizing...")

url = "https://getpocket.com/v3/oauth/authorize"

payload = {
    "consumer_key": consumer_key,
    "code": request_token,
}

response = requests.post(url, headers=headers, data=payload)

if response.status_code == 200:
    access_token = response.json()["access_token"]
    print(f"Access token: {access_token}")
else:
    print(f"Error obtaining access token: {response.text}")