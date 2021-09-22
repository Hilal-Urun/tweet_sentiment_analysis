# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:05:47 2020

@author: Hilal

You can scrape the tweets according to hastags with below code. 
Before starting you should get Twitter Api access keys an replace below str between lines 16-19
"""

import nltk
import tweepy
import pandas as pd
from nltk import word_tokenize

consumer_key = "CONSUMER_KEY"
consumer_key_secret = "CONSUMER_KEY_SECRET"
access_key = "ACCESS_KEY"
access_key_secret = "ACCESS_KEY_SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_key, access_key_secret)
api = tweepy.API(auth)


def preprocess(set):
    tweet_set = []
    for message in set['id']:
        filtered_sentence = []
        word_tokens = word_tokenize(message)
        if "https" in word_tokens:
            index_of_http = word_tokens.index("https")
            del word_tokens[index_of_http+2]
            word_tokens.remove("https")
        if "RT" in word_tokens:
            word_tokens.remove("RT")
        for word in word_tokens:
            if word == "@":
                index_of_at = word_tokens.index("@")
                del word_tokens[index_of_at+1]
                word_tokens.remove("@")
            elif word == "#":
                index_of_dash = word_tokens.index("#")
                del word_tokens[index_of_dash+1]
                word_tokens.remove("#")

        message = lis_to_string(word_tokens)
        message = nltk.re.sub('[^a-zA-âûîZİıŞşÇçÜüĞğÖö]+', ' ', message)
        if message not in tweet_set:
            tweet_set.append(message)
    return tweet_set



def lis_to_string(s):
    str1 = ""
    for ele in s:
        str1 += ele
        str1 += " "
    return str1

def tweets_df(res):
    id_list = [tweet.full_text for tweet in res]
    data_set = pd.DataFrame(id_list, columns=["id"])
    return data_set

def tweets_main(metin):
    hashtag = api.search(q=metin, lang="tr", count=200, result_type="recent", tweet_mode='extended')
    print(hashtag[0].full_text)
    sonuc = tweets_df(hashtag)
    sonuc_liste = preprocess(sonuc)
    sonuc_df = pd.DataFrame(sonuc_liste)
    print(sonuc_df[1])
   # sonuc_df.to_csv("deneme.csv", encoding="UTF-16", index=False, mode='a')


tweets_main("ekomomi")
