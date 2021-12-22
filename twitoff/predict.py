from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet

def predict_user(user0_name, user1_name, hypo_tweet_text):

    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # 2D Numpy Arrays
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # X matrix for training the logistic regressino
    vects = np.vstack([user0_vects, user1_vects])

    # 1D Numpy Arrays
    zeroes = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # y vector (target) for training the logistic regression
    labels = np.concatenate([zeroes, ones])

    # instantiate our logistic regression
    log_reg = LogisticRegression()

    # train our logistic regression
    log_reg.fit(vects, labels)

    # vectorize (get the word embeddings for)
    # our hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # get a prediction for which user is more likely to say the hypo_tweet_text
    prediction = log_reg.predict(hypo_tweet_vect.reshape(1, -1))

    return prediction[0]
