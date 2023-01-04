""" 
Unit 3.3.1
Date: 2022/12/20

App 'factory' for a flask instance.
Handles all the routing and browser requests for the Twitoff app using
flask.
"""

from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user

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
        return render_template("base.html", title="Reset Database")

    @app.route("/update")
    def update():
        for user in User.query.all():
            add_or_update_user(user.username)

        users = User.query.all()
        return render_template("base.html", title="Users Updated", users=users)

    @app.route("/user", methods=["POST"])
    @app.route("/user/<username>", methods=["GET"])
    def user(username=None, message=""):
        pass

    return app
