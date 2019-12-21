from models.users import *
import hashlib
from app import *


@login_manager.user_loader
def load_user(login):
    return Users.query.get(login)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile', login = current_user.login))

    if request.method == 'POST':
        login = request.form['login']

        if bool(Users.query.filter_by(login = login).first()):
            flash('Аккаунт уже существует', 'danger')
            
        elif len(login) < 2:
            flash('Логин слишком короткий', 'danger')

        else:
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if len(password) < 2:
                flash('Пароль слишком короткий', 'danger')

            elif password != confirm_password:
                flash('Пароли не совпадают', 'danger')
            
            else:
                password = hashlib.sha224(password.encode('utf-8')).hexdigest()
                new_user = Users(login, password, "User")
                db.session.add(new_user)
                db.session.commit()
                
                user = Users.query.filter_by(login = login).first()
                login_user(user, remember=True)
                flash('Успешно', 'success')
                return redirect(url_for('profile', login = login))
    else:
        login = request.args.get('login')
        
    return render_template('register.html', login = login)
