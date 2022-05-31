from flask import Flask
from flask_cors import CORS
from setup import setup_db
from setup_psql import setup_psql_db
from routes.authentication import authentication
from routes.count import count
from routes.stories import stories
from routes.zones import zones
from routes.forgot_password import forgot_password
from routes.user_details import user_details


app = Flask(__name__)

# Blueprints-------------------------------------------------------------/
app.register_blueprint(authentication, url_prefix="/authentication")
app.register_blueprint(count, url_prefix="/count")
app.register_blueprint(stories, url_prefix="/stories")
app.register_blueprint(zones, url_prefix="/zones")
app.register_blueprint(forgot_password, url_prefix="/forgot_password")
app.register_blueprint(user_details, url_prefix="/user_details")

CORS(app)


setup_db(app)

setup_psql_db()


if __name__ == '__main__':
    app.run(debug=True, port=3000)
