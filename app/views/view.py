from contests_parse import Parsing
from models.contests import Contests
from app import *

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        id = request.form.get('id').capitalize()
        ex = Parsing(id)

        all_good = True
        if bool(ex.status() != 200):
            flash('Неверный ID', 'danger') 
            all_good = False

        if bool(Contests.query.filter_by(id=id).first()): 
            flash('Контест уже в списке', 'danger') 
            all_good = False

        if all_good:
            new_contest = Contests(id,ex.get_name())
            db.session.add(new_contest)
            db.session.commit()
            flash('Успешно', 'success')
            ex.get_problems()
    
    contests = Contests.query.order_by(Contests.id).all()

    if current_user.is_authenticated:
        return render_template('index.html', Contests = contests, handle = current_user.get_id())
    else:
        return render_template('index.html', Contests = contests)





