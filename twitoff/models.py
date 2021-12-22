from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)
    # tweets = []

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    text = DB.Column(DB.Unicode(300), nullable=False)
    vect = DB.Column(DB.PickleType, nullable=False)
    # Creating a relationship between Users and Tweets
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # Create a whole list of tweets to be attached to the User
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)
