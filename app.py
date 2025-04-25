from flask import Flask, render_template, request
from geo_news_scaprer import scrape_geo_news
from db import insert_articles, get_article_by_url
from summarizer import generate_summary

app = Flask(__name__)

# Cache the URLs so that both forms can access them
cached_urls = []

@app.route("/", methods=["GET", "POST"])
def index():
    global cached_urls
    urls = cached_urls  # Start with whatever is in cache
    article_data = None
    search_attempted = False
    summary = None

    if request.method == "POST":
        if "target_url" in request.form:
            category_url = request.form.get("target_url")
            if category_url:
                articles = scrape_geo_news(category_url)
                insert_articles(articles)
                urls = [article['url'] for article in articles]
                cached_urls = urls  # update the cache

        elif "article_url" in request.form:
            article_url = request.form.get("article_url")
            article = get_article_by_url(article_url)
            search_attempted = True
            if article:
                article_data = {
                    "title": article.get("title", "N/A"),
                    "description": article.get("description", "N/A"),
                    "date": article.get("date", "N/A"),
                    "url": article.get("url", "N/A"),
                    "image": article.get("image_url", "")
                }
                # print("DEBUG - Article Data:", article_data)

                                # Check if summarization was requested
                if request.form.get("summarize") == "1":
                    summary = generate_summary(article_data["description"])


    return render_template("index.html", urls=urls, article_data=article_data, search_attempted=search_attempted, summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

