from flask import jsonify, request, Blueprint
from setup import mysql
import uuid

authentication = Blueprint("authentication", __name__)

secret_key = "TLS_AES_256_GCM_SHA384"


@authentication.route("/")
def index():
    return "Welcome to OverWatch APIs"


@authentication.route("/register", methods=["POST"])
def register():
    username = request.headers.get("username") or request.args.get("username")
    email = request.headers.get("email") or request.args.get("email")
    password = request.headers.get("password") or request.args.get("password")
    sec_question = request.headers.get("sec_question") or request.args.get("sec_question")
    sec_answer = request.headers.get("sec_answer") or request.args.get("sec_answer")

    uid = uuid.uuid4()

    if email and username and password and sec_question and sec_answer:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email= (%s)", [email])
        data = cur.fetchall()

        if data:
            return jsonify({"message": "Email already exists"}), 200
        else:
            cur.execute(
                "INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                (username, email, password, sec_question, sec_answer, uid)
            )
            mysql.connection.commit()
            cur.close()
            return jsonify({"message": "User created successfully"}), 200

    return jsonify({"message": "Fill all the fields"}), 400



