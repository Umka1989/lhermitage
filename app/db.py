import psycopg2
import hashlib
from contextlib import closing



pswd_check_for_login_query = "select rb, password_hash from users where rb = '{}'"


def get_connection (db_name, db_user_name, host_, password_):
    conn = psycopg2.connect(
        dbname = db_name,
        user = db_user_name,
        host = host_,
        password = password_
    )
    return conn


def connect_db():
    db_name = app.config['DB_NAME']
    db_user_name = app.config['DB_USER_NAME']
    host = app.config['DB_HOST']
    password = app.config['DB_PASSWORD']
    conn = get_connection(
        db_name,
        db_user_name,
        host,
        password
    )

    return conn


def get_script_results(connection, script, flag):
    cursor = connection.cursor()
    cursor.execute(script)
    result = cursor.fetchall() if flag == 'many' else cursor.fetchall()

    return result


def veryfi_user(user_rb):
    with closing(connect_db()) as db_conn:
        result = get_script_result(
            db_conn,
            pswd_check_for_login_query.format(user_rb)
        )
        return result






