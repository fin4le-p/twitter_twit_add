import tweepy
import os
import mysql.connector
import datetime
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_key = os.environ.get('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

twitCount: int = 0
twitCountPage: int = 0

def twitGet(contPage):

    global twitCount

    try:
    
        # DBcon
        conn = mysql.connector.connect(
            host='0.0.0.0',
            port='3306',
            user='user',
            password='password',
            database='schema',
            charset='utf8mb4'
        )
    
        cur = conn.cursor(buffered=True)
    
        yestDay = datetime.date.today() - datetime.timedelta(days=1)
    
        tweet_data = []
    
        Account = "fin4le_p"  # 取得したいユーザーのユーザーIDを代入
        tweets = api.user_timeline(Account, count=200, page=contPage)
        for tweet in tweets:
    
            twitCount += 1
    
            twitDay = tweet.created_at.date()
    
            if yestDay != twitDay:
                break

            if "@" in tweet.text[0]:
                twid: int = tweet.id
                user: str = tweet.user.screen_name
                date = tweet.created_at
                text: str = tweet.text
                favo = int = tweet.favorite_count
                retw = int = tweet.retweet_count
    
                cur.execute("INSERT INTO TWITTER_TIMELINE VALUES (%s, %s, %s, %s, %s, %s, 1)",
                            (twid, user, date, text, favo, retw))
                conn.commit()

            elif "RT @" in tweet.text[0:4]:
                twid: int = tweet.id
                user: str = tweet.user.screen_name
                date = tweet.created_at
                text: str = tweet.text
                favo = int = tweet.favorite_count
                retw = int = tweet.retweet_count
    
                cur.execute("INSERT INTO TWITTER_TIMELINE VALUES (%s, %s, %s, %s, %s, %s, 2)",
                            (twid, user, date, text, favo, retw))
                conn.commit()
    
            elif not "RT @" in tweet.text[0:4] and not "@" in tweet.text[0]:
                twid: int = tweet.id
                user: str = tweet.user.screen_name
                date = tweet.created_at
                text: str = tweet.text
                favo = int = tweet.favorite_count
                retw = int = tweet.retweet_count
    
                cur.execute("INSERT INTO TWITTER_TIMELINE VALUES (%s, %s, %s, %s, %s, %s, 0)",
                            (twid, user, date, text, favo, retw))
                conn.commit()

        return twitCount
    
    except tweepy.error.TweepError as e:
        print("err")
        print(e.reason)
    except mysql.connector.Error as e:
        print("Error code:", e.errno)        # error number
        print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
        print("Error message:", e.msg)       # error message
        print("Error:", e)                   # errno, sqlstate, msg values
        s = str(e)
        print("Error:", s)                   # errno, sqlstate, msg values
    finally:
        cur.close()
        conn.close()

twitMaxCount = twitGet(twitCountPage + 1)

while True:
    if twitMaxCount == 200:
        twitCount = 0
        twitMaxCount = twitGet(twitCountPage + 1)
    else:
        break