from flask import Flask
from flask import render_template, redirect, url_for

app = Flask(__name__)

#root of our website
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/assignment3_1.html')
def profile():
    return render_template('assignment3_1.html', user_name= 'nOa', owl_name='owl1',
                           cards=['../static/img/empress.png', '../static/img/justice.png', '../static/img/moon.png'])

if __name__ == '__main__':
    app.run(debug=True)

    