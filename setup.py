from flask_mysqldb import MySQL


mysql = MySQL()


def setup_db(app):

    app.config['SECRET_KEY'] = 'TLS_AES_256_GCM_SHA384'
    app.config['MYSQL_HOST'] = 'overwatch-db-do-user-10414546-0.b.db.ondigitalocean.com'
    app.config['MYSQL_USER'] = 'doadmin'
    app.config['MYSQL_PASSWORD'] = 'AVNS_9vnkKwrkRGiq8_j'
    app.config['MYSQL_DB'] = 'defaultdb'
    app.config['MYSQL_PORT'] = 25060
    app.config['JSON_SORT_KEYS'] = False

    mysql.init_app(app)

# def setup_db(app):
#     app.config['SECRET_KEY'] = 'TLS_AES_256_GCM_SHA384'
#     app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
#     app.config['MYSQL_USER'] = 'sql6470760'
#     app.config['MYSQL_PASSWORD'] = 'lWrGY6ZNE6'
#     app.config['MYSQL_DB'] = 'sql6470760'
#     app.config['MYSQL_PORT'] = 3306
#     app.config['JSON_SORT_KEYS'] = False
#
#     mysql.init_app(app)

# def setup_db(app):
#     # app.config['SECRET_KEY'] = 'TLS_AES_256_GCM_SHA384'
#     app.config['MYSQL_HOST'] = 'localhost'
#     app.config['MYSQL_USER'] = 'root'
#     app.config['MYSQL_PASSWORD'] = ''
#     app.config['MYSQL_DB'] = 'overwatchDB'
#
#     mysql.init_app(app)
