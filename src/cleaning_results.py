import pandas as pd
import re
import numpy as np
import os

path = "../andooni/summary"

def calc_score(x:str=None):

    s = x.replace("\\u200c","").replace("\n","")
    s = re.sub('[^\w]+', ' ', s, flags=re.U)

    words = ["ایران_قوی", "شهید_قاسم_سلیمانی", "لبيك_يا_خامنه" , "لبیک_یا_خامنه",
             "لبیک یا خامنه" , "لبيک_يا_خامنه" , "لبيک_يا_خامنه" , "امام خامنه" , "لبیک_یاخامنه" , "لبيک_يا_خامنه"]
    anti_words = ["مهسا_امینی", "كيرم_تو_بيت_رهبرى", "نیکا_شاکرمی" , "مرگ_بر_خامنه_ای" , "لبیک یا خامنه" , "ایران_قوی"]

    arzeshi_value = 0
    for word in set(words):
        word = word.replace("\\u200c","").replace("\n","")
        word = re.sub('[^\w]+', ' ', word, flags=re.U)
        if s.find(word) >= 0:
            # print(word, " +2")
            arzeshi_value += 1

    for word in set(anti_words):
        word = word.replace("\\u200c","").replace("\n","")
        word = re.sub('[^\w]+', ' ', word, flags=re.U)
        if s.find(word) >= 0:
            # print(word, " -1")
            arzeshi_value -= 1

    return arzeshi_value


df_list = []
for csv in os.listdir(path):
    if csv.endswith(".csv"):
        f = path + "/" + csv
        df_list.append(pd.read_csv(f))


df = pd.concat(df_list)
df = df[df.username != "username"]

df.hashtags = df.hashtags.apply(
    lambda a: a.replace("[", "").replace("]", "").replace("'", "").replace(",", "").rstrip().lstrip())
df.hashtags = df.hashtags.apply(lambda x : x.replace("\\u200c",""))
df.text = df.text.apply(lambda x : x.replace("\\u200c","").replace("\n",""))
df["arzeshi_score_text"] = df.text.apply(lambda x : calc_score(x))
df["arzeshi_score_tag"] = df.hashtags.apply(lambda x : calc_score(x))
df["arzeshi_score"] = df["arzeshi_score_text"] + df["arzeshi_score_tag"]

users = df.groupby("username").median()
arzeshi_users = users[users.arzeshi_score > 0]
arzeshi_users.reset_index(inplace=True)
df_arzeshi = df[df.username.isin(arzeshi_users.username.to_list())]
df_arzeshi.retweetcount = df_arzeshi.retweetcount.astype(int)
df_arzeshi.sort_values(by="retweetcount", ascending=False, inplace=True)
df_arzeshi.drop_duplicates(subset="retweetcount", inplace=True, keep="first")

arzeshi_usernames = df_arzeshi.username.to_list()
s = " ".join(arzeshi_usernames)
# x = "@"+s

df_arzeshi.to_csv("../andooni/output/arzeshi_table.csv")

with open("../andooni/output/username_string.txt", "w") as text_file:
    text_file.write(s)