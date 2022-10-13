import pandas as pd
import os

path = "/Users/hessam.k.rad/Desktop/twitter_scraper/summary"

df_list = []
for csv in os.listdir(path):
    if csv.endswith(".csv"):
        f = path + "/" + csv
        df_list.append(pd.read_csv(f))

df = pd.concat(df_list)
df = df[df.username != "username"]
df.hashtags = df.hashtags.apply(
    lambda a: a.replace("[", "").replace("]", "").replace("'", "").replace(",", "").rstrip().lstrip().split())
users = df.groupby("username").median()
users.reset_index(inplace=True)
df.retweetcount = df.retweetcount.astype(int)
df.sort_values(by="retweetcount", ascending=False, inplace=True)
# df.drop_duplicates(subset="retweetcount", inplace=True, keep="first")