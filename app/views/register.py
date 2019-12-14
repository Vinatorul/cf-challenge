from models.users import *
from app import *


@login_manager.user_loader
def load_user(handle):
    return Users.query.get(handle)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile', handle = current_user.handle))

    if request.method == 'POST':
        handle = request.form['handle']

        if bool(Users.query.filter_by(handle = handle).first()):
            user = Users.query.filter_by(handle = handle).first()
            if user.password != None:
                flash('Аккаунт уже существует', 'danger')
            else:
                password = request.form['password']
                confirm_password = request.form['confirm_password']

                if len(password) < 2:
                    flash('Пароль слишком короткий', 'danger')

                elif password != confirm_password:
                    flash('Пароли не совпадают', 'danger')
                
                else:
                    user.set_password(password) # Changing default password
                    db.session.add(user)
                    db.session.commit()
                    
                    user = Users.query.filter_by(handle=handle).first()
                    login_user(user, remember=True)
                    flash('Успешно', 'success')
                    return redirect(url_for('profile', handle = handle))
            
        elif len(handle) < 2:
            flash('Хендл слишком короткий', 'danger')

        else:
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if len(password) < 2:
                flash('Пароль слишком короткий', 'danger')

            elif password != confirm_password:
                flash('Пароли не совпадают', 'danger')
            
            else:
                new_user = Users(handle)
                new_user.set_password(password) # Changing default password
                db.session.add(new_user)
                db.session.commit()
                
                user = Users.query.filter_by(handle=handle).first()
                login_user(user, remember=True)
                flash('Успешно', 'success')
                return redirect(url_for('profile', handle = handle))
    else:
        handle = request.args.get('handle')
        
    return render_template('register.html', handle = handle)
