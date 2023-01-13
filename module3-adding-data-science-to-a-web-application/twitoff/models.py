""" 
Unit 3.3.3
Date: 2022/01/12

Set up sqlalchemy classes & database integration
"""

from flask_sqlalchemy import SQLAlchemy

# make database obj from SQLA class

DB = SQLAlchemy()


class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)
    # tweets = [], defined by backref in Tweet

    def __repr__(self) -> str:
        return f"User: {self.username}"


class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column: unicode for emojis & special chars
    text = DB.Column(DB.Unicode(300))
    # word embeddings / vectorization
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id foreign key column
    user_id = DB.Column(
        DB.BigInteger, DB.ForeignKey("user.id"), nullable=False
    )
    # user column creates two-way link between user and tweet
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self) -> str:
        return f"Tweet: {self.text}"
