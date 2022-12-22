""" 
Unit 3.3.1
Date: 2022/12/20

App 'factory' for a flask instance
"""

from flask import Flask, render_template
from .models import DB, User, Tweet

# factory
def create_app():
    app = Flask(__name__)

    # database config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # register database with Flask app
    DB.init_app(app)

    @app.route("/")
    def root():
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    @app.route("/bananas")
    def bananas():
        return render_template("base.html", title="Bananas")

    @app.route("/reset")
    def reset():
        # Drop all database tables
        DB.drop_all()

        # Recreate all database tables according to schema in models.py
        DB.create_all()
        return "Database has been reset"

    @app.route("/populate")
    def populate():
        # Create two dummy users in the DB
        michael = User(id=1, username="Michael")
        DB.session.add(michael)
        julian = User(id=2, username="Julian")
        DB.session.add(julian)

        # Create two tweets users in the DB
        tweet1 = Tweet(id=1, text="michael's tweet text", user=michael)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text="julian's tweet text", user=julian)
        DB.session.add(tweet2)

        # Save changes and commit
        DB.session.commit()
        return "Database populated"

    return app
