from flask import jsonify, Blueprint
from setup import mysql


count = Blueprint('count', __name__)


@count.route("/")
def count_index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(id) FROM users")
    data = cur.fetchone()

    return jsonify({"count": data})
