""" 
Unit 3.3.1
Date: 2022/12/20

App 'factory' for a flask instance
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

    @app.route("/populate")
    def populate():
        # Create two default users in the DB
        add_or_update_user("austen")
        add_or_update_user("nasa")

        users = User.query.all()
        return render_template(
            "base.html", title="Populate Database", users=users
        )

    @app.route("/update")
    def update():
        for user in User.query.all():
            add_or_update_user(user.username)

        users = User.query.all()
        return render_template("base.html", title="Users Updated", users=users)

    # FOR WARM-UP EXERCISE:
    @app.route("/iris")
    def iris():
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression

        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(
            random_state=0, solver="lbfgs", multi_class="multinomial"
        ).fit(X, y)

        return str(clf.predict(X[:2, :]))

    return app
