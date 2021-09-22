import re
import tweepy
import sqlite3 as lite
import string
def cleanDB():
    databaseFile = 'tweets.db'
    db = lite.connect(databaseFile)
    im = db.cursor()
    im.execute('DELETE FROM known_tweets')
    db.commit()
    db.close()

databaseFile = 'tweets.db'
db = lite.connect(databaseFile)
im = db.cursor()

consumer_key = "qbdKaVksabWOIdzvb0iFZWrOT"
consumer_secret = "zGMDoQKL7IqKuwAPjuWU3EY9ncJg6KbNYkxiU09XlrpxrRqSWF"
access_key = "3337185467-MI45nmchpe0ER1BArspUV9MgiHt6JQV1b52QnYm"
access_secret = "Tvawn11btljApZoQEeFo01qToi3Ufz4PeO4IgBPVlWNZo"

tweet_liste = []
user = ["user1","user2","user3","...continued"]

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    auth.get_authorization_url()
    api = tweepy.API(auth, wait_on_rate_limit=True)
except tweepy.TweepError:
    print('Hata')


def remove_nonchar(text):
    characters = "a|b|c|ç|d|e|f|g|ğ|h|ı|i|j|k|l|m|n|o|ö|p|r|s|ş|t|u|ü|v|y|z" \
                 "|A|B|C|Ç|D|E|F|G|Ğ|H|I|İ|J|K|L|M|N|O|Ö|P|R|S|Ş|T|U|Ü|V|Y|Z|w|W|x|X|q|Q|,"
    text = re.sub('[^' + characters + '\s]', '', text)
    return text


def remove_links(text):
    return ' '.join([w for w in text.split(' ') if not 'http' in w])


def getTweets():
    global user
    for user in user:
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items():
            current_tweet = tweet.full_text
            current_tweet.replace('\"', '').replace('\'', '').replace('-', ' ')
            if re.match(r'RT @[_A-Za-z0-9]+:', current_tweet):
                continue
            else:
                current_tweet = current_tweet.replace('\"', '').replace('\'', '').replace('-', ' ').replace('\n',' ')
                current_tweet = remove_nonchar(current_tweet)
                current_tweet = remove_links(current_tweet)

                im.execute('INSERT INTO known_tweets (user,tweet) VALUES ("%s","%s")' %
                           (user, current_tweet))
                db.commit()

if __name__=='__main__':
    getTweets()
    db.close()
