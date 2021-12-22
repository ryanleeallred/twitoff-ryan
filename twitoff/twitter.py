from os import getenv
import tweepy
from .models import DB, User, Tweet
import spacy

# getting our environment variables
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# making the connection to the twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):

    try:

        twitter_user = TWITTER.get_user(screen_name=username)

        # If there's no user in the database create one
        # IF there *is* a user in the database, let's have that be our db_user
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username))

        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200, 
                                       exclude_replies=True, 
                                       include_rts=False, 
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, 
                             text=tweet.full_text[:300], 
                             vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error Processing {username}: {e}")
        raise e

    else:
        DB.session.commit()


# Take tweet text and turn it into 
# a word embedding "vector"
nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
    
