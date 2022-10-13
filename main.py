from dotenv import load_dotenv
load_dotenv(".env")
from src.scraper import *


if __name__ == '__main__':
    consumer_key = os.environ["consumer_key"]
    consumer_secret = os.environ["consumer_secret"]
    access_key = os.environ["access_key"]
    access_secret = os.environ["access_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    words = "لبیک_یا_خامنه‌_ای"
    print(f"Scraping twitter for {words}#")

    cursor = Tweet_Cursor(api=api, words=words)

    try:
        cursor.iterator()

    except:
        last_results = cursor.last_results

    print('Scraping has completed!')