from flask import jsonify, Blueprint
from setup_psql import setup_psql_db


count = Blueprint('count', __name__)


@count.route("/")
def count_index():
    '''
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(id) FROM users")
    users_count = cur.fetchone()
    # data = {"users_count": cur.fetchone()}

    cur.execute("SELECT COUNT(id) FROM stories")
    stories_count = cur.fetchone()
    # data["stories_count"] = cur.fetchone()

    cur.execute("SELECT COUNT(id) FROM zones")
    zones_count = cur.fetchone()

    cur.close()
    '''

    conn = setup_psql_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM users")
    users_count = cur.fetchone()

    cur.execute("SELECT COUNT(id) FROM stories")
    stories_count = cur.fetchone()

    cur.execute("SELECT COUNT(id) FROM zones")
    zones_count = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify(
        {
            "users_count": users_count[0],
            "stories_count": stories_count[0],
            "zones_count": zones_count[0]
        }
    )
