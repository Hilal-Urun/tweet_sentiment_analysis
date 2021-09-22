import tweepy
import MySQLdb
import sys
import os
import logging

consumer_key = os.getenv("qbdKaVksabWOIdzvb0iFZWrOT")
consumer_secret = os.getenv( "zGMDoQKL7IqKuwAPjuWU3EY9ncJg6KbNYkxiU09XlrpxrRqSWF")
access_token = os.getenv("3337185467-MI45nmchpe0ER1BArspUV9MgiHt6JQV1b52QnYm")
access_token_secret = os.getenv("Tvawn11btljApZoQEeFo01qToi3Ufz4PeO4IgBPVlWNZo")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

connection =  MySQLdb.connect(host= "localhost",
    user="kullanıcı adı",
    passwd="şifre",
    db="twitter")
cursor = connection.cursor()

class TwitterStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            cursor.execute("INSERT INTO tweets (tweet_id, tweet_text, screen_name, author_id, created_at, inserted_at) VALUES (%s, %s, %s, %s, %s, NOW());", (status.id, status.text, status.author.screen_name, status.author.id, status.created_at))
            connection.commit()
        except:
            pass

    def on_error(self, status_code):
        # Rate limit reached
        if status_code == 420:
            logging.exception("Sınıra ulaşıldı! ") 
try:
    streamListener = TwitterStreamListener()
    twitterStream = tweepy.Stream(auth = api.auth, listener=streamListener)
except tweepy.error.TweepError as e:
    logging.exception(e)
except UnicodeEncodeError as e:
    logging.exception(e)
except:
    logging.exception(sys.exc_info()[0])
    raise
finally:
    cursor.close()
    connection.close()
