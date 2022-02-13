from flask import request, jsonify, Blueprint
from setup import mysql
import uuid

zones = Blueprint("zones", __name__)


@zones.route("/")
def index():
    return "Welcome to ZONES APIs of OverWatch"


@zones.route("/post_zone", methods=['POST'])
def post_zone():
    latitude = request.headers.get("latitude") or request.args.get("latitude")
    longitude = request.headers.get("longitude") or request.args.get("longitude")
    user_uid = request.headers.get("user_uid") or request.args.get("user_uid")

    zuid = uuid.uuid4()

    if latitude and longitude and user_uid:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO zones (latitude, longitude, zuid, user_uid) VALUES (%s, %s, %s, %s)",
            ([latitude], [longitude], [zuid], [user_uid])
        )
        mysql.connection.commit()
        cur.close()

        return jsonify(
            {
                "message": "Zone stored successfully",
                "status": 200
            }
        ), 200

    return jsonify(
        {
            "message": "Fill all the required fields",
            "status": 400
        }
    ), 400


@zones.route("/get_all_zones", methods=['GET'])
def get_all_zones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM zones ORDER BY id DESC")
    data = cur.fetchall()

    final_data = []
    for record in data:
        final_data.append(
            {
                "id": record[0],
                "latitude": record[1],
                "longitude": record[2],
                "zuid": record[3],
                "user_uid": record[4]
            }
        )

    return jsonify(
        {
            "data": final_data,
            "status": 200
        }
    ), 200


@zones.route("/delete_zone", methods=['DELETE'])
def delete_zone():
    zuid = request.headers.get("zuid") or request.args.get("zuid")

    if zuid:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM zones WHERE zuid=%s", [zuid])
        mysql.connection.commit()
        cur.close()

        return jsonify(
            {
                "message": "Zone deleted successfully",
                "status": 200
            }
        ), 200

    return jsonify(
        {
            "message": "Fill all the required fields",
            "status": 400
        }
    ), 400
