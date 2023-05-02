from flask import Flask, render_template, request
from articles import get_saved_articles, extract_article_info
import os
from dotenv import load_dotenv
from summarize import summarize_text, scrape_text

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
access_token = os.getenv('ACCESS_TOKEN') # Obtained from tokens.py

app = Flask(__name__)

@app.route("/")
def articles():
    saved_articles = get_saved_articles(consumer_key, access_token)
    article_list = extract_article_info(saved_articles)
    return render_template("articles.html", articles=article_list)

@app.route("/summary")
def summary():
    url = request.args.get("url")
    saved_articles = get_saved_articles(consumer_key, access_token)
    article_list = extract_article_info(saved_articles)
    article = next((a for a in article_list if a["url"] == url), None)
    if article:
        article_text = scrape_text(article["url"])
        article_summary = summarize_text(article_text, 500)
        article["summary"] = article_summary
        return render_template("summary.html", article=article)
    else:
        return "Article not found", 404

if __name__ == "__main__":
    app.run(debug=True)