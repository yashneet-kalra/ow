from flask import Flask
from flask_cors import CORS
from setup import setup_db
from routes.authentication import authentication
from routes.count import count
from routes.stories import stories
from routes.zones import zones


app = Flask(__name__)

# Blueprints-------------------------------------------------------------/
app.register_blueprint(authentication, url_prefix="/authentication")
app.register_blueprint(count, url_prefix="/count")
app.register_blueprint(stories, url_prefix="/stories")
app.register_blueprint(zones, url_prefix="/zones")


CORS(app)


setup_db(app)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
