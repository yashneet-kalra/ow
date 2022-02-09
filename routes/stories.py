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


@stories.route("/get_all_stories", methods=['GET'])
def get_all_stories():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT stories.id, stories.suid, stories.story, stories.location, stories.date_created, users.username, \
        users.email FROM stories INNER JOIN users ON stories.user_uid=users.uid ORDER BY id DESC"
    )
    data = cur.fetchall()
    stories_data = []
    for record in data:
        stories_data.append(
            {
                "id": record[0],
                "suid": record[1],
                "story": record[2],
                "location": record[3],
                "date_created": record[4].strftime('%a,%e-%b-%Y'),
                "username": record[5],
                "email": record[6]
            }
        )

    return jsonify({"data": stories_data})


@stories.route("/get_story", methods=['GET'])
def get_story():
    user_uid = request.headers.get("user_uid") or request.args.get("user_uid")

    if user_uid:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, suid, story, location, date_created FROM stories WHERE user_uid=%s ORDER BY id DESC", [user_uid])
        data = cur.fetchall()
        cur.close()
        stories_data = []

        for record in data:
            stories_data.append(
                {
                    "id": record[0],
                    "suid": record[1],
                    "story": record[2],
                    "location": record[3],
                    "date_created": record[4].strftime('%a,%e-%b-%Y')
                }
            )

        return jsonify({"data": stories_data})

    return jsonify({"message": "Fill all the details"})


@stories.route("/delete_story", methods=['DELETE'])
def delete_story():
    suid = request.headers.get("suid") or request.args.get("suid")

    if suid:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM stories WHERE suid=%s", [suid])
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Story deleted successfully"})

    return jsonify({"message": "Fill all the required fields"})
