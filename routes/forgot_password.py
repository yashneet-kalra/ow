from flask import request, jsonify, Blueprint
from setup_psql import setup_psql_db


forgot_password = Blueprint("forgot_password", __name__)


@forgot_password.route("/index")
def index():
    return "Welcome to FORGOT PASSWORD APIs of OverWatch"


@forgot_password.route("/", methods=['GET'])
def forgot_pass():
    email = request.headers.get("email") or request.args.get("email")

    if email:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM users WHERE email=%s)", [email])
        data = cur.fetchone()

        if data[0] == 1:
            cur.execute("SELECT sec_question FROM users WHERE email=%s", [email])
            data = cur.fetchone()
            cur.close()
            conn.close()
            return jsonify(
                {
                    "sec_question": data[0],
                    "status": 200
                }
            ), 200
        else:
            cur.close()
            conn.close()
            return jsonify(
                {
                    "message": "User with this email does not exists",
                    "status": 404
                }
            ), 404

    return jsonify(
        {
            "message": "Fill all the required fields",
            "status": 400
        }
    ), 400


@forgot_password.route("/answer", methods=['GET'])
def answer():
    sec_answer = request.headers.get("sec_answer") or request.args.get("sec_answer")
    email = request.headers.get("email") or request.args.get("email")

    if sec_answer and email:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("SELECT sec_answer FROM users WHERE email=%s", [email])
        data = cur.fetchone()

        if data[0] == sec_answer:
            cur.close()
            conn.close()
            return jsonify(
                {
                    "message": "Answer matched successfully",
                    "status": 200
                }
            ), 200
        else:
            cur.close()
            conn.close()
            return jsonify(
                {
                    "message": "Incorrect answer",
                    "status": 400
                }
            ), 400

    return jsonify(
        {
            "message": "Fill all the required fields",
            "status": 400
        }
    ), 400


@forgot_password.route("/change", methods=['POST'])
def change():
    email = request.headers.get("email") or request.args.get("email")
    new_pass = request.headers.get("new_pass") or request.args.get("new_pass")

    if email and new_pass:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password=%s WHERE email=%s", (new_pass, email))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(
            {
                "message": "Password changed successfully",
                "status": 200
            }
        ), 200

    return jsonify(
        {
            "message": "Fill all the required fields",
            "status": 400
        }
    ), 400
