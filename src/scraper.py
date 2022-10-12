import os, errno
import time
import datetime
import pandas as pd
import tweepy
import json
from tqdm import tqdm


class Tweet_Cursor():

    def __init__(self, api : tweepy.API = None, words:[str]=None):
        self.words = words
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

    def iterator(self):

        print(f"Start time : {self.init_time.isoformat()[:19]}")

        while True:
            try:
                list_tweets = self.cursor.iterator.next()
                count = len(list_tweets)
                self.counter += count
                print(f" -- finished {self.counter} tweets -- ", end="\r")

            except:
                self.total_tweets += self.counter
                print(f" -- exhausted after {self.counter} iterations, total tweets read : {self.total_tweets} --")
                print(" -- reaching threshold, resting for a few minutes -- ")
                for sec in tqdm(range(850)):
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

            filename = f'andooni/short_data_{datetime.datetime.now().isoformat()[:10].replace(":","_")}.csv'

            df.to_csv(filename, mode="a", encoding='utf-8', index=False)

            json_list = [item._json for item in list_tweets]

            full_df = pd.DataFrame(json_list)
            full_df.to_hdf(f'andooni/full_data/full_data_{datetime.datetime.now().isoformat()[:10].replace(":","_")}.h5', complevel=5, key='df', mode="a", index=False)