from app import app, logger
import psycopg2
from hashlib import md5
from flask import render_template, redirect, session, url_for, request
from contextlib import closing
"""
db block
"""
pswd_check_for_login_query = "select rb, password_hash, position from users where rb = '{}'"

set_paswrd_query = "update users set password_hash = '{0}' where rb = '{1}'"


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
    result = cursor.fetchall() if flag == 'many' else cursor.fetchone()

    return result


def set_password(login, pswrd):
    with closing (connect_db()) as db_conn:
        cursor = db_conn.cursor()
        try:
            query = set_paswrd_query.format(pswrd, login.upper())
            logger.debug(query)
            cursor.execute(query)
        except Exception as e:
            logger.debug('ошибка при задании пароля {}'.format(str(e)))
        finally:
            cursor.close()
            db_conn.commit()



def get_user_info(user_rb):
    with closing(connect_db()) as db_conn:
        result = get_script_results(
            db_conn,
            pswd_check_for_login_query.format(user_rb),
            'single'
        )
        return result
"""
end db block
"""

def authorizate(login, pswrd ):
    hashed_pswrd = md5(pswrd.encode()).hexdigest()
    logger.debug('hashed password {}'.format(hashed_pswrd))
    query_result = get_user_info(login.upper())
    logger.debug(query_result)
    if query_result is None:
        flag, reason = False, 'Пользователь с таким RB не найден'
    else:
        if hashed_pswrd == query_result[1]:
            flag, reason = True, ''
            session['logged_in'] = True
            session['role']  = query_result[2]
        else:
            flag, reason = False, 'Некорректно указан RB пользователя или пароль'
    return flag, reason


def registrate(login, pswrd, pswrd_check):
    if pswrd == pswrd_check:
        logger.debug('pswrd {}'.format(pswrd))
        hashed_pswrd = md5(pswrd.encode()).hexdigest()
        logger.debug('hashed pswrd {}'.format(hashed_pswrd))
        query_result = get_user_info(login.upper())
        if query_result is None:
            flag, reason = False, 'Пользователю не доступна регистрация'
        elif query_result[1]:
            flag, reason = False, 'Пользователь уже существует'
        else:
            set_password(login, hashed_pswrd)
            flag, reason = True, 'Пользователю задан пароль'
            session['logged_in'] = True
            session['role'] = query_result[2]
    else:
        flag, reason = False, 'Введенные пароли не совпадают'

    return flag, reason



@app.route('/')
def index():
    if not session.get('logged_in'):
        print(session)
        print(url_for('login'))
        return redirect(login())
    else:
        return render_template('index.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    logger.debug('я в логине')
    session['mistake'] = ''
    session['status'] = 'login'
    for each in request.form:
        logger.debug('{0} => {1}'.format(each, request.form[each]))
    if request.method == 'GET':
        logger.debug('request method GET')
        return render_template(
            'login.html',
            status=session['status'],
            mistake=session['mistake']
        )
    else:
        logger.debug('request method POST')
        session['status'] = request.form['type']
        if request.form['type'] == 'login':
            result_flag, reason = authorizate(request.form['login'], request.form['pswrd'])
            logger.debug('AUTH res is {}'.format(result_flag))
            logger.debug('AUTH res is {}'.format(reason))
        else:
            result_flag, reason = registrate(
                request.form['login'],
                request.form['pswrd'],
                request.form['pswrd_check']
            )
            logger.debug('REG res is {}'.format(result_flag))
            logger.debug('REG res is {}'.format(reason))
        if result_flag:
            return redirect(url_for('index'))
        else:
            session['mistake'] = reason
            logger.debug(session)
            return render_template(
                    'login.html',
                    status=session['status'],
                    mistake=session['mistake']
            )


@app.route('/meeting_minuts')
def meeting_minuts():
    return render_template('meeting_minuts.html')







"""
@app.route('/')
@app.route('/index')
def main_page():
    if not session.get['logged_in']:
        return render_template('index.html')
    else:
        return redirect('login_register.html')

@app.route('/login_register', methods=['POST', 'GET'])
def login_register():
    if request.method == 'GET':
        return render_template('login_register.html')
    else:
"""