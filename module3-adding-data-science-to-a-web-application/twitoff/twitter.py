""" 
Unit 3.3.3
Date: 2022/01/12

Functions to query Twitter API, vectorize tweets, and sync them to 
local database instance.
"""

from os import getenv
from .models import DB, User, Tweet
import dotenv
import tweepy
import spacy

dotenv.load_dotenv()

# Get API keys from .env
key = getenv("TWITTER_API_KEY")
secret = getenv("TWITTER_API_KEY_SECRET")

# Connect to twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("my_model/")


def add_or_update_user(username):
    """Using twitter API, adds a twitter user and their most recent 200 tweets
    (excluding retweets) to the database. If user is already present in
    the database, updates db with most recent tweets.

    Parameters
    ----------
    username : str
        Twitter API screen name

    Raises
    ------
    e
        Any error will prevent user and tweets tables from being updated
    """
    try:
        # Get user information from twitter
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check if user already exists in Users table
        # Otherwise, create a new user
        db_user = User.query.get(twitter_user.id) or User(
            id=twitter_user.id, username=username
        )

        # Add the user to the database
        DB.session.add(db_user)

        # Get user tweets, up to 200 most recent non-retweets
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id,
        )

        # update User's newest_tweet_id
        if len(tweets) > 0:
            db_user.newest_tweet_id = tweets[0].id

        # Add all tweets (plus vectorized versions) to db
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text[:300],
                vect=tweet_vector,
                user_id=twitter_user.id,
            )
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        # Save and commit changes
        DB.session.commit()


def vectorize_tweet(tweet_text):
    """Generates word embedding of tweet text using spacy

    Parameters
    ----------
    tweet_text : str


    Returns
    -------
    array
    """
    return nlp(tweet_text).vector
