import os
import errno
import time
import sys
import datetime
import pandas as pd
import tweepy
import warnings
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class Tweet_Cursor():

    def __init__(self, api : tweepy.API = None, words:[str]=None):
        self.words = words
        self.iter_count = 0
        self.counter = 0
        self.total_tweets = 0
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
            os.makedirs("andooni")
            os.makedirs("andooni/full_data")
            os.makedirs("andooni/summary")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


    def save_to_csv(self, list_tweets):

        if len(list_tweets) == 0:
            return None

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

        filename = f'andooni/summary/short_data_{datetime.datetime.now().isoformat()[:10].replace(":", "_")}.csv'

        df.to_csv(filename, mode="a", encoding='utf-8', index=False)


    def save_to_hdf(self, agg_list):

        if len(agg_list) == 0:
            return None

        json_list = [item._json for item in agg_list]
        full_df = pd.DataFrame(json_list)
        full_df.to_hdf(
            f'andooni/full_data/{datetime.datetime.now().isoformat()[:19].replace(":", "_").replace("-", "_")}.h5',
            complevel=9, key='df', mode="w", index=False)


    def sleep(self, note:str=None):
        self.iter_count += 1
        self.total_tweets += self.counter
        print(f" -- exhausted due to : {note} -- ")
        print(
            f" -- tweets read in this iteration : {self.counter} -- ")
        print(f" -- total tweets read : {self.total_tweets} -- ")
        print(f" -- number of iterations : {self.iter_count} -- ")
        print(" -- resting for 15 minutes -- ")
        for i in tqdm(range(870)):
            time.sleep(1)
        self.counter = 0


    def iterator(self):

        print(f"Start time : {self.init_time.isoformat()[:19]}")
        agg_list = []

        while True:

            if abs(self.counter - 2600) > 50:

                try:
                    list_tweets = self.cursor.iterator.next()
                    self.save_to_csv(list_tweets)
                    agg_list.extend(list_tweets)
                    count = len(list_tweets)
                    self.counter += count
                    print(f" -- finished {self.counter} tweets -- ", end="\r")

                except Exception as e:
                    if e.response.status_code in (401,403):
                        print('Twitter Authentication failed')
                        sys.exit(1)
                    self.save_to_hdf(agg_list)
                    agg_list = []
                    self.sleep(note=str(e))

            else:
                json_list = [item._json for item in agg_list]
                self.save_to_hdf(json_list)
                agg_list = []
                self.sleep(note="counter limit")
