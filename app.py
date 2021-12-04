import json
import os
import sys
import base64

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


def check_auth(auth):
    if auth == None:
        return jsonify({"message": "Authentication Faild"}), 401
    elif auth.startswith("Basic "):
        auth = auth.replace("Basic ", "", 1)
        decode_data = base64.b64decode(auth).decode()
        i = decode_data.find(":")
        user_id, password = decode_data[:i], decode_data[i+1:]
        if db_manager.is_exist(user_id, password):
            return user_id, 200
        else:
            return jsonify({"message": "Authentication Faild"}), 401
    else:
        return jsonify({"message": "Authentication Faild"}), 401


@app.route("/users/<username>", methods=["GET"])
def get(username):
    auth = request.headers.get("Authorization")
    check = check_auth(auth)
    if check[1] != 200:
        return check
    user = db_manager.get_user(username)
    if user == []:
        return jsonify({"message": "No User found"}), 404
    else:
        result = {
            "message": "User details by user_id",
            "user": {
                "user_id": user[0].user_id,
                "nickname": user[0].nickname,
            }
        }
        if user[0].comment != None:
            result["user"]["comment"] = user[0].comment
    return jsonify(result), 200


@app.route("/users/<username>", methods=["PATCH"])
def update(username):
    auth = request.headers.get("Authorization")
    check = check_auth(auth)
    if check[1] != 200:
        return check
    if username != check[0]:
        return jsonify({
            "message": "No Permission for Update"
        }), 403
    user = db_manager.get_user(username)
    print("get user", user)
    if user == []:
        return jsonify({"message": "No User found"}), 404
    json = request.get_json()
    return user_manager.update_user(username, json)


@app.route("/close", methods=["POST"])
def delete():
    auth = request.headers.get("Authorization")
    check = check_auth(auth)
    if check[1] != 200:
        return check
    return user_manager.delete_user(check[0])


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

