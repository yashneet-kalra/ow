from flask import request, jsonify
from functools import wraps
import jwt
# from setup import mysql


secret_key = 'TLS_AES_256_GCM_SHA384'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            token = request.headers.get('x-access-token')
            if not token:
                return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, secret_key, ['HS256'])
            #
            # cur = mysql.connection.cursor()
            # cur.execute("SELECT EXISTS(SELECT * FROM session_manager WHERE token = %s)", [token])
            # token_exists = cur.fetchone()
            #
            # if token_exists[0] == 0:
                # raise TokenNotFound
        # except TokenNotFound:
        #     return jsonify({'message': "Token NOT found in session_manager Table in Database"}), 403
        except:
            return jsonify({"message": "Token is Invalid!"}), 403
        return f(*args, **kwargs)

    return decorated
