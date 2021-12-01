import json
import os
import sys

from flask import Flask, abort, jsonify, request

import db_manager
import user_manager

app = Flask(__name__)

#環境変数設定
app.config['SQLALCHEMY_DATABASE_URI'] = db_manager.db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/", methods=["POST", "GET"])
def index():
    abort(404)
    return None

@app.route("/signup", methods=["POST"])
def signup():
    json = request.get_json()
    return user_manager.signup_user(json)


@app.route("/users/<username>", methods=["GET"])
def get(username):
    auth = request.headers.get("Authorization")
    print(auth)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

