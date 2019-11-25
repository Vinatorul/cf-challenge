from app import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/contest/')
def contest():
    return render_template('contest.html')