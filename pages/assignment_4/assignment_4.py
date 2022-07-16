from flask import Blueprint, render_template, jsonify
from flask import request

def get_all_user(db):
    query = f'select * from users'
    users_list = db(query, query_type='fetch')
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
    return return_list

def get_user(db, id):
    query = "SELECT * FROM users WHERE id=%s;" % id
    users_list = db(query, query_type='fetch')
    for user in users_list:
        user_dict = {
            'id': user.id,
            'first_name': user.fname,
            'last_name': user.lname,
            'password': user.password,
            'email': user.email
        }
    return user_dict

def getPage4(db, session):
    assignment4 = Blueprint(
        'assignment4',
        __name__,
        static_folder= 'static',
        static_url_path= '/pages/about',
        template_folder='templates'
    )

    @assignment4.route('/assignment4', methods=["GET"])
    def index():
        if 'fname' in session:
            first_name = session['fname']
            last_name = session['lname']

        else:
            first_name = None
            last_name = None

        users = get_all_user(db)
        return render_template('assigment4.html', users=users, first_name=first_name, last_name=last_name, message="")

    @assignment4.route('/assignment4', methods=["POST"])
    def posted():
        message=""
        print(request.form['function'])
        if 'fname' in session:
            first_name = session['fname']
            last_name = session['lname']

        else:
            first_name = None
            last_name = None

        # create new user
        if request.form['function'] == 'create':
            fname_input = request.form['fname']
            lname_input = request.form['lname']
            email_input = request.form['email']
            password_input = request.form['password']
            message = (f' create new user {fname_input} {lname_input}')
            query = "INSERT INTO users(fname,lname,email,password) VALUES ('%s', '%s', '%s', %s)" % (fname_input, lname_input, email_input, password_input)
            db(query=query, query_type='commit')

        elif (request.form['function'] == 'update'):
            try:
                id = request.form['uid']
                user = get_user(db, id)
                name = user['first_name'] + ' ' + user['last_name']
                message = (f' update user: {name}')
                update_sql=''
                if(request.form['fname_u']):
                    update_sql = 'fname = "' + request.form['fname_u'] + '",'
                if (request.form['lname_u']):
                    update_sql += 'lname = "' + request.form['lname_u'] + '",'
                if (request.form['email_u']):
                    update_sql += 'email = "' + request.form['email_u'] + '",'
                if (request.form['password_u']):
                    update_sql += 'password = "' + request.form['password_u'] + '",'
                update_sql = update_sql[:-1]
                query = "UPDATE users SET %s WHERE id = %s" % ( update_sql, id)
                db(query=query, query_type='commit')
            except:
                message = ('failed to update this user, check if it exist or if you chnaged it correctly')

        elif (request.form['function'] == 'delete'):
            try:
                id = request.form['uid_d']
                user = get_user(db, id)
                name = user['first_name'] + ' ' + user['last_name']
                message = (f' delete user: {name}')
                query = "DELETE FROM users WHERE id='%s';" % id
                db(query, query_type='commit')
            except:
                print('exeption')
                message = ('failed to delete this user, check if it exists')

        users = get_all_user(db)
        return render_template('assigment4.html', users=users, first_name=first_name, last_name=last_name,
                               message=message)

    return assignment4

