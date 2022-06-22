from flask import Flask
from flask import render_template, redirect, url_for, request, session, jsonify
from datetime import timedelta

app = Flask(__name__)

potential_cultists = {'user1':{'fname':'maya', 'lname': 'assulyn', 'email': 'pedacop128@mahazai.com'},
'user2':{'fname':'noa', 'lname': 'elharar', 'email': 'pongau@24hinbox.com'},
'user3':{'fname':'benny', 'lname': 'xar', 'email': 'progport@bomukic.com'},
'user4':{'fname':'shelly', 'lname': 'shabty', 'email': 'w5ui8@bitcoinandmetals.com'},
'user5':{'fname':'tomer', 'lname': 'shefi', 'email': 'elsukov5@uhpanel.com'}
}

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

#root of our website
@app.route('/')
def home_page():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/assignment3_1')
def profile():
    first_name = None
    last_name = None

    if 'fname' in session:
        first_name = session['fname']
        last_name = session['lname']

    return render_template('assignment3_1.html', first_name=first_name, last_name=last_name, owl_name='owl1',
                           cards=['../static/img/empress.png', '../static/img/justice.png', '../static/img/moon.png'])

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

if __name__ == '__main__':
    app.run(debug=True)

    