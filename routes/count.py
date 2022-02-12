from flask import jsonify, Blueprint
from setup import mysql


count = Blueprint('count', __name__)


@count.route("/")
def count_index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(id) FROM users")
    users_count = cur.fetchone()
    # data = {"users_count": cur.fetchone()}
    cur.execute("SELECT COUNT(id) FROM stories")
    stories_count = cur.fetchone()
    # data["stories_count"] = cur.fetchone()
    cur.close()
    return jsonify(
        {
            "users_count": users_count[0],
            "stories_count": stories_count[0]
        }
    )
