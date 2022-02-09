from flask import request, jsonify, Blueprint
from setup import mysql
import uuid
import datetime


stories = Blueprint("stories", __name__)


@stories.route("/")
def index():
    return "Welcome to the STORIES API section of OverWatch APIs"


@stories.route("/post_story", methods=['POST'])
def post_story():
    story = request.headers.get("story") or request.args.get("story")
    location = request.headers.get("location") or request.args.get("location")
    user_uid = request.headers.get("user_uid") or request.args.get("user_uid")

    date_created = datetime.date.today().strftime('%Y-%m-%d')

    suid = uuid.uuid4()

    if story and location and date_created and user_uid:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO stories VALUES (NULL, %s, %s, %s, %s, %s)",
            ([suid], [story], [location], [date_created], [user_uid])
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Story stored successfully"})

    return jsonify({"message": "Fill all the fields"})
