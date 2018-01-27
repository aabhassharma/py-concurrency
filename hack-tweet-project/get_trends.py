import os
import sys
import twitter
import sqlite3
import gevent
from gevent.queue import Queue, Empty
import logging

tasks = Queue(maxsize=50)
logger = logging.getLogger('get_trends')
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %message)s')
streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)

def get_twitter_creds():
    '''
    Get credentials as set in env because you're not an idiot and don't want to
    commit those
    '''
    creds_dict = {}
    creds_dict['consumer_key'] = os.environ['twitter_consumer_key']
    creds_dict['consumer_secret'] = os.environ['twitter_consumer_secret']
    creds_dict['access_token_key'] = os.environ['twitter_access_token_key']
    creds_dict['access_token_secret'] = os.environ['twitter_access_token_secret']
    return creds_dict


def get_twitter_api(twitter_creds):
    '''
    Reusable instance of the API wrapper
    '''
    api = twitter.Api(
        consumer_key=twitter_creds['consumer_key'],
        consumer_secret=twitter_creds['consumer_secret'],
        access_token_key=twitter_creds['access_token_key'],
        access_token_secret=twitter_creds['access_token_secret'])
    return api


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def write_to_tweet_table(cursor, trend, tweet_id, tweet):
    trend_column = 'trend'
    tweet_column = 'tweet'
    tweet_id_column = 'tweet_id'
    cursor.execute(
        '''INSERT OR IGNORE INTO trend_and_tweet (trend, tweet_id, tweet) VALUES ("{}", {}, "{}")'''.format(
            trend, tweet_id, tweet
        ))

def set_trends_and_tweets(api, cursor):
    trends_and_tweets = []
    trending_articles = api.GetTrendsCurrent()
    for trend in trending_articles:
        # I don't want the bullshit that has any promoted content with it
        if trend.promoted_content:
            logger.info('Found promoted content in trend {}'.format(trend))
            continue
        # There's some unsanitized data in here
        # Simple sanitation
        if "\\" in trend.name:
            logger.info('Found unsanitized data content in trend {}'.format(trend))
            continue
        if not is_ascii(trend.name):
            logger.info('Found non ASCII content in trend {}'.format(trend))
            continue
        # Find the most popular tweets that are mentioning this trend
        # But I also want to limit it to within 500 miles of my location
        searched_tweets = api.GetSearch(
            term=trend.name,
            geocode="37.774929,-122.419416,500mi",
            result_type="popular")
        # Got empty list, skip
        if not searched_tweets:
            logger.info('Found no tweets for trend {}'.format(trend))
            continue
        # VOILA! You have the most popular tweets within 100 miles of my location
        # that are referencing the most popular trending hashtags right Now
        for status in searched_tweets:
            # skip truncated text ugh API constraints
            if status.truncated:
                logger.info('Found truncated text in status {}'.format(status))
                continue
            # write_to_tweet_table(cursor, trend.name, status.id, status.text.encode('utf-8'))


if __name__ == "__main__":
    sqlite_file = 'tweet_db.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    try:
        twitter_creds = get_twitter_creds()
    except KeyError:
        print "Please make sure the Twitter creds are set in the env"
        sys.exit(1)
    api = get_twitter_api(twitter_creds=twitter_creds)
    set_trends_and_tweets(api, c)
    conn.commit()
    conn.close()
