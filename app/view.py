from app import *


@app.route('/', methods=['GET', 'POST'])
def index():
    count = db.session.query(Users).count()
    return render_template('index.html', Contests = Contests, count = count)


@app.route('/users', methods=['GET', 'POST'])
def users():
    
    if request.method == "POST":

        handle = request.form.get('handle')
        name = request.form.get('name')

        new_user = Users(handle, name)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users', Users = Users))

    return render_template('users.html', Users = Users)


@app.route('/contest/')
def contest():
    return render_template('contest.html')