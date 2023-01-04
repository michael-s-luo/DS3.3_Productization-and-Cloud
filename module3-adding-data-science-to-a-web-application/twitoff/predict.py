""" 
Unit 3.3.2
Date: 2022/12/23

Handles training of logistic regression model to predict
user of a given tweet. 
"""

from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import vectorize_tweet


def predict_user(username_0, username_1, tweet_text):
    """Given two twitter users, predicts the user more likely to tweet a given
    hypothetical tweet using a logistic regression model. Input tweets are
    vectorized using SpaCy. Data is obtained from local database instance.

    Parameters
    ----------
    username_0 : str
        Twitter username
    username_1 : str
        Twitter username
    tweet_text : str
        Hypothetical tweet text
    """

    # Get user data from db
    user_0 = User.query.filter(User.username == username_0).one()
    user_1 = User.query.filter(User.username == username_1).one()

    # Get tweet word embeddings from each user
    user_0_vects = np.array([tweet.vect for tweet in user_0.tweets])
    user_1_vects = np.array([tweet.vect for tweet in user_1.tweets])

    # Create training data from both users
    X_train = np.vstack([user_0_vects, user_1_vects])

    # Create training labels
    zeros = np.zeros(user_0_vects.shape[0])
    ones = np.ones(user_1_vects.shape[0])
    y_train = np.concatenate([zeros, ones])

    # Instantiate and fit log reg model
    model_lr = LogisticRegression().fit(X_train, y_train)

    # Vectorize hypothetical tweet text
    tweet_text_vect = [vectorize_tweet(tweet_text)]

    return model_lr.predict(tweet_text_vect)[0]
