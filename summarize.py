import os
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") # Must have .env containing this variable and your API key in the same directory.

def summarize_text(text, max_words):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please summarize the following text in {max_words} words or less:\n{text}",
        temperature=0.5,
        max_tokens=500,
        n=1,
        stop=None,
        timeout=15,
    )
    summary = response.choices[0].text.strip()
    return summary

def scrape_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = ""
    for paragraph in soup.find_all("p"):
        text += paragraph.text.strip() + " "
    return text