from contests_parse import Parsing
from app import *


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        contestId = request.form.get('contestId').capitalize()
        ex = Parsing(contestId)

        all_good = True
        if bool(ex.status() != 200):
            flash('Неверный ID', 'danger') 
            all_good = False

        if bool(Contests.query.filter_by(contestId=contestId).first()): 
            flash('Контест уже в списке', 'danger') 
            all_good = False

        if all_good:
            new_contest = Contests(contestId,ex.get_name())
            db.session.add(new_contest)
            db.session.commit()
            flash('Успешно', 'success')
            ex.get_problems()

    contests = Contests.query.order_by(Contests.contestId).all()

    return render_template('index.html', Contests = contests)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        handle = request.form.get('handle').capitalize()
        name = request.form.get('name').capitalize()

        all_good = True
        if bool(Users.query.filter_by(handle=handle).first()): 
            flash('Хендл уже используется', 'danger') 
            all_good = False
            
        if bool(Users.query.filter_by(name=name).first()):
            flash('Имя уже используется', 'danger')
            all_good = False

        if len(handle) < 2:
            flash('Хендл слишком короткий', 'danger')
            all_good = False

        if len(name) < 2:
            flash('Имя слишком короткое', 'danger')
            all_good = False

        if all_good:
            new_user = Users(handle, name)
            db.session.add(new_user)
            db.session.commit()
            flash('Успешно', 'success')

    users = Users.query.order_by(Users.handle).all()  

    return render_template('users.html', users = users)


@app.route(f'/contest/<int:contestId>', methods=['GET', 'POST'])
def contest(contestId):
    print(contestId)
    return render_template('contest.html', results = Parsing(contestId).get_solutions(), contestId = contestId, problems = Parsing(contestId).get_problems())