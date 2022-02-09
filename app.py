from flask import Flask
from flask_cors import CORS
from setup import setup_db
from routes.authentication import authentication
from routes.count import count


app = Flask(__name__)

# Blueprints-------------------------------------------------------------/
app.register_blueprint(authentication, url_prefix="/authentication")
app.register_blueprint(count,url_prefix="/count")


CORS(app)


setup_db(app)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
