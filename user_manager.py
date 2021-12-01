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
    result = {
        "message": "Account successfully created",
        "user": {
            "user_id": user_id,
            "nickname": user_id
        }
    }
    return jsonify(result), 200
