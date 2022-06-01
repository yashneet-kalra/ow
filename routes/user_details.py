from flask import request, jsonify, Blueprint
from setup_psql import setup_psql_db


user_details = Blueprint("user_details", __name__)


@user_details.route("/")
def index():
    user_uid = request.headers.get("user_uid") or request.args.get("user_uid")

    if user_uid:
        conn = setup_psql_db()
        cur = conn.cursor()
        cur.execute("SELECT username, email FROM users WHERE uid=%s", [user_uid])
        user_data = cur.fetchall()
        print(user_data)

        final_user_data = [
            {
                "username": user_data[0][0],
                "email": user_data[0][1]
            }
        ]

        cur.execute(
            "SELECT id, suid, story, location, date_created, incident_date, edited, anonymity \
            FROM stories WHERE user_uid=%s ORDER BY id DESC", [user_uid]
        )
        stories_data = cur.fetchall()
        print(stories_data)

        final_stories_data = []
        for record in stories_data:
            final_stories_data.append(
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

        cur.execute(
            "SELECT * FROM zones WHERE user_uid=%s ORDER BY id DESC", [user_uid]
        )
        zones_data = cur.fetchall()
        print(zones_data)

        final_zones_data = []
        for record in zones_data:
            final_zones_data.append(
                {
                    "id": record[0],
                    "latitude": record[1],
                    "longitude": record[2],
                    "zuid": record[3],
                    "loc_name": record[5]
                }
            )

        cur.close()
        conn.close()

        return jsonify(
            {
                "user_details": final_user_data,
                "stories_details": final_stories_data,
                "zones_details": final_zones_data
            }
        ), 200

    return jsonify(
        {
            "message": "Fill all the required fields",
            "status": 400
        }
    ), 400
