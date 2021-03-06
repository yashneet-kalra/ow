from flask import request, jsonify, Blueprint
from setup_psql import setup_psql_db
import uuid
import datetime


stories = Blueprint("stories", __name__)


@stories.route("/")
def index():
    return "Welcome to the STORIES API section of OverWatch APIs", 200


@stories.route("/post_story", methods=['POST'])
def post_story():
    story = request.headers.get("story") or request.args.get("story")
    location = request.headers.get("location") or request.args.get("location")
    user_uid = request.headers.get("user_uid") or request.args.get("user_uid")
    incident_date = request.headers.get("incident_date") or request.args.get("incident_date")
    anonymity = request.headers.get("anonymity") or request.args.get("anonymity")

    date_created = datetime.date.today().strftime('%Y-%m-%d')
    incident_date = datetime.datetime.strptime(incident_date, '%Y-%m-%d')

    suid = str(uuid.uuid4())

    if story and location and date_created and user_uid and incident_date and anonymity:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO stories (suid, story, location, date_created, user_uid, incident_date, anonymity) \
            VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (suid, story, location, date_created, user_uid, incident_date, anonymity)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Story stored successfully"}), 200

    return jsonify({"message": "Fill all the fields"}), 400


@stories.route("/get_all_stories", methods=['GET'])
def get_all_stories():
    conn = setup_psql_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT stories.id, stories.suid, stories.story, stories.location, stories.date_created, stories.incident_date,\
         stories.edited, stories.anonymity, users.username, users.email FROM stories INNER JOIN users \
         ON stories.user_uid=users.uid ORDER BY id DESC"
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
                "incident_date": record[5].strftime('%a,%e-%b-%Y'),
                "edited": record[6],
                "anonymity": record[7],
                "username": record[8],
                "email": record[9]
            }
        )

    cur.close()
    conn.close()

    return jsonify({"data": stories_data}), 200


@stories.route("/get_story", methods=['GET'])
def get_story():
    user_uid = request.headers.get("user_uid") or request.args.get("user_uid")

    if user_uid:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, suid, story, location, date_created, incident_date, edited, anonymity \
            FROM stories WHERE user_uid=%s ORDER BY id DESC",
            [user_uid]
        )
        data = cur.fetchall()

        cur.close()
        conn.close()

        stories_data = []

        for record in data:
            stories_data.append(
                {
                    "id": record[0],
                    "suid": record[1],
                    "story": record[2],
                    "location": record[3],
                    "date_created": record[4].strftime('%a,%e-%b-%Y'),
                    "incident_date": record[5].strftime('%a,%e-%b-%Y'),
                    "edited": record[6],
                    "anonymity": record[7]
                }
            )

        return jsonify({"data": stories_data}), 200

    return jsonify({"message": "Fill all the details"}), 400


@stories.route("/delete_story", methods=['DELETE'])
def delete_story():
    suid = request.headers.get("suid") or request.args.get("suid")

    if suid:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM stories WHERE suid=%s", [suid])
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Story deleted successfully"}), 200

    return jsonify({"message": "Fill all the required fields"}), 400


@stories.route("/update_story", methods=['POST'])
def update_story():
    suid = request.headers.get("suid") or request.args.get("suid")
    story = request.headers.get("story") or request.args.get("story")
    location = request.headers.get("location") or request.args.get("location")

    if suid and story and location:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE stories SET story= %s, location= %s, edited='YES' WHERE suid= %s",
            (story, location, suid)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Story and Location updated successfully"}), 200

    elif suid and story and not location:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("UPDATE stories SET story= %s, edited='YES' WHERE suid= %s", (story, suid))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Story updated successfully"}), 200

    elif suid and location and not story:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("UPDATE stories SET location= %s, edited='YES' WHERE suid= %s", (location, suid))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Location updated successfully"}), 200

    return jsonify({"message": "Fill all the required fields"}), 400
