from flask import jsonify, request, Blueprint
# from setup import mysql
from setup_psql import setup_psql_db
import uuid

authentication = Blueprint("authentication", __name__)

# secret_key = "TLS_AES_256_GCM_SHA384"


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

    uid = str(uuid.uuid4())

    if email and username and password and sec_question and sec_answer:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email= (%s)", [email])
        data = cur.fetchall()

        if data:
            conn.close()
            return jsonify({"message": "Email already exists"}), 200
        else:
            cur.execute(
                "INSERT INTO users (username, email, password, sec_question, sec_answer, uid) VALUES (%s, %s, %s, %s, "
                "%s, %s)",
                (username, email, password, sec_question, sec_answer, uid)
            )
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": "User created successfully"}), 200

    return jsonify({"message": "Fill all the fields"}), 400


@authentication.route("/registered_users", methods=["GET"])
def registered_users():
    conn = setup_psql_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users order by id DESC")
    a = cur.fetchall()

    data = []

    for user_details in a:
        user = {
            "id": user_details[0],
            "username": user_details[1],
            "email": user_details[2],
            "password": user_details[3],
            "sec_question": user_details[4],
            "sec_answer": user_details[5],
            "uid": user_details[6]
        }

        data.append(user)

    cur.close()
    conn.close()
    return jsonify({"data": data})


@authentication.route("/login", methods=["GET"])
def login():
    email = request.headers.get("email") or request.args.get("email")
    password = request.headers.get("password") or request.args.get("password")

    if email and password:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM users WHERE email=%s and password=%s)", (email, password))
        exists = cur.fetchone()

        if exists[0] == 1:
            cur.execute("SELECT * FROM users WHERE email = %s", [email])
            data = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify({
                "status": 200,
                "message": "User logged in successfully",
                "username": data[0][1],
                "email": data[0][2],
                "uid": data[0][6]
            }), 200

        cur.close()
        conn.close()
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Fill all the fields"}), 400
