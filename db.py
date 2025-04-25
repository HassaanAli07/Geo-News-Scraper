import os
from pymongo import MongoClient
from dotenv import load_dotenv


# loading environment variables
load_dotenv()

conn = os.getenv('MONGO_URI')

client = MongoClient(conn)


db = client['cognilium_database']

collection = db['articles']

collection.create_index('url', unique=True)


def insert_articles(articles):
    for article in articles:
        try:
            if not collection.find_one({'url': article['url']}):
                collection.insert_one(article)
        except Exception as e:
            print(f"Insert failed: {e}")

# listing all the extracted articles link
def get_all_articles():
    return list(collection.find({}, {'_id': 0, 'url': 1}))

# extracting info of extracted article via url
def get_article_by_url(url):
    return collection.find_one({'url': url})
