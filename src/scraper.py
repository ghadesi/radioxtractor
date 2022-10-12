import os, errno
import time
import datetime
import pandas as pd
import tweepy
from tqdm import tqdm


class Tweet_Cursor():

    def __init__(self, api : tweepy.API = None, words:[str]=None):
        self.words = words
        self.counter = 0
        self.df = pd.DataFrame(columns=['username',
                                   'description',
                                   'location',
                                   'following',
                                   'followers',
                                   'totaltweets',
                                   'retweetcount',
                                   'text',
                                   'hashtags',
                                   'source'])

        orig_time = (datetime.datetime.now() - datetime.timedelta(days=30))
        self.init_time = datetime.datetime.now()
        self.cursor = tweepy.Cursor(api.search_tweets,
                               words,
                               since_id=orig_time.date().isoformat(),
                               tweet_mode='extended')


        try:
            os.makedirs("scraping_results")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def iterator(self):

        print(f"Start time : {self.init_time.isoformat()[:19]}")

        while True:
            try:
                list_tweets = self.cursor.iterator.next()
                count = len(list_tweets)
                self.counter += count
                print(f" -- finished {self.counter} tweets -- ", end="\r")

            except:
                print(f" -- paused after {self.counter} tweets --")
                print(" -- reaching threshold, resting for 15 minutes -- ")
                for sec in tqdm(range(120)):
                    time.sleep(1)
                self.counter = 0
                list_tweets = self.cursor.iterator.next()

            i = 1
            df = self.df.copy()

            for tweet in list_tweets:
                username = tweet.user.screen_name
                description = tweet.user.description
                location = tweet.user.location
                following = tweet.user.friends_count
                followers = tweet.user.followers_count
                totaltweets = tweet.user.statuses_count
                retweetcount = tweet.retweet_count
                hashtags = tweet.entities['hashtags']
                source = tweet.retweet_count

                try:
                    text = tweet.retweeted_status.full_text
                except AttributeError:
                    text = tweet.full_text
                hashtext = list()
                for j in range(0, len(hashtags)):
                    hashtext.append(hashtags[j]['text'])

                ith_tweet = [username, description,
                             location, following,
                             followers, totaltweets,
                             retweetcount, text, hashtext, source]

                df.loc[len(df)] = ith_tweet
                i = i + 1

            filename = f'scraping_results/short_data_{datetime.datetime.now().isoformat()[:10].replace(":","_")}.csv'

            df.to_csv(filename, mode="a", encoding='utf-8', index=False)

            json_list = []
            for item in list_tweets:
                json_list.append(item._json)

            full_df = pd.DataFrame(json_list)
            full_df.to_csv(f'scraping_results/full_data_{datetime.datetime.now().isoformat()[:10].replace(":","_")}.csv',
                           mode="a", encoding='utf-8', index=False)