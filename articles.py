import requests
import json
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
access_token = os.getenv('ACCESS_TOKEN') # Obtained from tokens.py

def get_saved_articles(consumer_key, access_token):
    base_url = "https://getpocket.com/v3/get"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Accept": "application/json",
    }

    payload = f"consumer_key={consumer_key}&access_token={access_token}&detailType=complete"

    response = requests.post(base_url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()["list"]
    else:
        raise Exception(f"Error while fetching articles: {response.text}")

def extract_article_info(articles):
    article_list = []
    for article_id, article in articles.items():
        title = article.get("resolved_title", article["given_title"])
        url = article.get("resolved_url", article["given_url"])
        publication = urlparse(url).netloc  # Extract the domain name from the URL
        
        if publication.startswith("www."):
            publication = publication[4:]

        article_list.append(
            {
                "title": title, 
                "publication": publication, 
                "url": url, 
                "summary": ""}
        )

    return article_list

if __name__ == "__main__":
    saved_articles = get_saved_articles(consumer_key, access_token)
    article_list = extract_article_info(saved_articles)
    print(len(article_list))
    