from flask import abort, jsonify

import db_manager

def signup_user(json):
    try:
        # データが含まれているかチェック
        user_id = json['user_id']
        password = json['password']
        user_id_length = len(user_id)
        password_length = len(password)
    except KeyError:
        return jsonify({
            "message": "Account creation failed",
            "cause": "required user_id and password"
        }), 400
    if user_id_length < 6 or 20 < user_id_length:
        return jsonify({
            "message": "Account creation failed",
            "cause": "length user_id"
        }), 400
    if password_length < 8 or 20 < password_length:
        return jsonify({
            "message": "Account creation failed",
            "cause": "length password"
        }), 400
    for k in user_id:
        code = ord(i)
        if code < 33 or 126 < code:
            return jsonify({
                "message": "Account creation failed",
                "cause": "pattern user_id"
            }), 400
    for k in password:
        code = ord(i)
        if code < 33 or 126 < code:
            return jsonify({
                "message": "Account creation failed",
                "cause": "pattern password"
            }), 400
    user = db_manager.get_user(user_id)
    if user != []:
        return jsonify({
            "message": "Account creation failed",
            "cause": "already same user_id is used"
        }), 400
    result = {
        "message": "Account successfully created",
        "user": {
            "user_id": user_id,
            "nickname": user_id
        }
    }
    db_manager.add_new_user(user_id, password, "")
    return jsonify(result), 200


def update_user(username, json):
    try:
        nickname = json['nickname']
        comment = json['comment']
    except KeyError:
        return jsonify({
            "message": "User updation failed",
            "cause": "required nickname or comment"
        }), 400
    if "user_id" in json.keys() or "password" in json.keys():
        return jsonify({
            "message": "User updation failed",
            "cause": "not updatable user_id and password"
        }), 400
    db_manager.update_user(username, nickname, comment)
    if nickname == "":
        nickname = username
    return jsonify({
        "message": "User successfully updated",
        "recipe": [
            {
                "nickname": nickname,
                "comment": comment
            }
        ]
    }), 200

def delete_user(username):
    db_manager.delete_user(username)
    return jsonify({"message": "Account and user successfully removed"}), 200
