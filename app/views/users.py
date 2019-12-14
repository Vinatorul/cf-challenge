from contests_parse import Parsing
from models.users import Users
from models import *
from app import *

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        handle = request.form.get('handle')
        name = request.form.get('name')

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
            new_user = Users(handle)
            new_user.name = name
            db.session.add(new_user)
            db.session.commit()
            flash('Успешно', 'success')

    users = Users.query.order_by(Users.handle).all()  

    return render_template('users.html', users = users)