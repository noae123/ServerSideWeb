from flask import Flask
from flask import render_template, redirect, url_for, request, session, jsonify
from datetime import timedelta
from pages.assignment_4.assignment_4 import getPage4
import mysql.connector
import requests
import os
# I had a problem with dotenv, I set my environment manually
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)

potential_cultists = {'user1':{'fname':'maya', 'lname': 'assulyn', 'email': 'pedacop128@mahazai.com', 'password': '1234'},
'user2':{'fname':'noa', 'lname': 'elharar', 'email': 'pongau@24hinbox.com', 'password': '1234'},
'user3':{'fname':'benny', 'lname': 'xar', 'email': 'progport@bomukic.com', 'password': '1234'},
'user4':{'fname':'shelly', 'lname': 'shabty', 'email': 'w5ui8@bitcoinandmetals.com', 'password': '1234'},
'user5':{'fname':'tomer', 'lname': 'shefi', 'email': 'elsukov5@uhpanel.com', 'password': '1234'}
}

app.secret_key = os.environ.get('SECRET_KEY')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

#root of our website
@app.route('/')
def home_page():
    return redirect('/home')

@app.route('/home')
def home():
    if 'fname' in session:
        first_name = session['fname']
        last_name = session['lname']

    else:
        first_name = None
        last_name = None

    return render_template('home.html', first_name=first_name, last_name=last_name)

@app.route('/contact')
def contact():
    if 'fname' in session:
        first_name = session['fname']
        last_name = session['lname']

    else:
        first_name = None
        last_name = None

    return render_template('contact.html', first_name=first_name, last_name=last_name)

@app.route('/assignment3_1')
def profile():
    if 'fname' in session:
        first_name = session['fname']

    if 'lname' in session:
        last_name = session['lname']

    first_name = None
    last_name = None

    if 'fname' in session:
        first_name = session['fname']
        last_name = session['lname']

    return render_template('assignment3_1.html', first_name=first_name, last_name=last_name,
                           cards=[{'src':'../static/img/empress.png', 'name':'the empress'},
                                  {'src':'../static/img/justice.png', 'name':'justice'},
                                  {'src': '../static/img/moon.png', 'name': 'the moon'}])

@app.route('/assignment3_2', methods=["POST", "GET"])
def Login():
    first_name = None
    last_name = None

    if 'fname' in session:
        first_name = session['fname']

    if 'lname' in session:
        last_name = session['lname']

    if request.method == "POST":
        first_name = request.form['fname']
        last_name = request.form['lname']
        session['fname'] = first_name
        session['lname'] = last_name
        return render_template('assignment3_2.html', first_name=first_name, last_name=last_name)

    elif 'search' in request.args:
        search = request.args['search'].lower()
        searc_dict = []

        if (len(search.split())> 1):
            full_name_search = search.split()
            for user in potential_cultists:
                if full_name_search[0] in potential_cultists[user]['fname'] and full_name_search[1] in potential_cultists[user]['lname']:
                    searc_dict.append(user)

                if full_name_search[0] in potential_cultists[user]['lname'] and full_name_search[1] in potential_cultists[user]['fname']:
                    searc_dict.append(user)

        for user in potential_cultists:
            if search in potential_cultists[user]['fname'] or search in potential_cultists[user]['lname'] or search in potential_cultists[user]['email']:
                searc_dict.append(user)
        return render_template('assignment3_2.html', searc_dict=[potential_cultists[x] for x in searc_dict], first_name=first_name, last_name=last_name)
    return render_template('assignment3_2.html', first_name=first_name, last_name=last_name)

@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('Login'))

# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host=os.environ.get('DB_HOST'),
                                         user=os.environ.get('DB_USER'),
                                         passwd=os.environ.get('DB_PASSWORD'),
                                         database=os.environ.get('DB_NAME'))
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

app.register_blueprint(getPage4(interact_db,session))

@app.route('/assignment4/users')
def json_func(id_parm=None):
    if (id_parm != None):
        query = "SELECT * FROM users WHERE id=%s;" % id_parm
    else:
        query = f'select * from users'

    users_list = interact_db(query, query_type='fetch')
    if len(users_list) != 0:
        return_list = []
        for user in users_list:
            user_dict = {
                'id': user.id,
                'first_name': user.fname,
                'last_name': user.lname,
                'password': user.password,
                'email': user.email
            }
            return_list.append(user_dict)
    return jsonify(return_list)

@app.route('/assignment4/outer_source', methods=["POST", "GET"])
def outer():
    if 'fname' in session:
        first_name = session['fname']
        last_name = session['lname']

    else:
        first_name = None
        last_name = None

    json_dict = None
    user_id = None
    if request.method == "POST":
        if request.form['function'] == 'frontend':
            user_id = request.form['uid_d']
        else:
            url = 'https://reqres.in/api/users/' + request.form['input_id']
            json_dict = requests.get(url).json()

    return render_template('assignment4_outer.html', first_name=first_name, last_name=last_name, json_dict=json_dict, user_id=user_id)

@app.route('/assignment4/', defaults={'USER_ID': None})
@app.route('/assignment4/<int:USER_ID>')
def user_id(USER_ID: int):
    if USER_ID == None:
        return redirect('/assignment4/restapi_users')
    else:
        try:
            return json_func(USER_ID)
        except UnboundLocalError:
            return jsonify('no such id in the database')


@app.route('/assignment4/restapi_users')
def defult_user():
    return json_func().json[0]

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG'))

    