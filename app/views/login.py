from models.users import *
import hashlib
from app import *
import time


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', handle = current_user.handle))

    if request.method == 'POST':

        handle = request.form['handle']
        
        if handle != '': 
            if bool(Users.query.filter_by(handle=handle).first()):
                print(Users.query.filter_by(handle = handle).first().password)
                if Users.query.filter_by(handle = handle).first().password != None:
                    user = Users.query.filter_by(handle=handle).first()
                else:
                    return redirect(url_for('register', handle = handle))

                try:
                    password = hashlib.sha224(request.form['password'].encode('utf-8')).hexdigest()
                    if password == user.password: 
                        login_user(user, remember=True)
                        flash('Успешно', 'success')
                        return redirect(url_for('profile', handle = handle))
                    else:  
                        flash('Неверный пароль', 'danger')
                        return render_template('login.html', handle = handle)
                except:
                    pass
                
                return render_template('login.html', handle = handle)        
            else:
                return redirect(url_for('register', handle = handle))
            
    return render_template('login.html')