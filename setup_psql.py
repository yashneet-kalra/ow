import psycopg2


def setup_psql_db():

    conn = psycopg2.connect(
        host="ec2-52-204-195-41.compute-1.amazonaws.com",
        database="d1vb6fgg31fa3v",
        user="pftcrdgtxhxaqc",
        password="d4e0e8ddb2349f87f06ebe977750573232e9bac6138d598240fe941f7462682a",
        port="5432"
    )

    return conn
