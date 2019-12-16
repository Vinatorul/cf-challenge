from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import login_required
from werkzeug import secure_filename
from contests_parse import get_rating
from models.users import *
import hashlib
from app import *
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        handleCFORCE = request.form['handleCFORCE']
        handleTIMUS = request.form['handleTIMUS']
        handleINFORM = request.form['handleINFORM']
        vk_url = request.form['vk_url']
        about = request.form['about']
        
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if 'new_icon' in request.files:
            new_icon = request.files['new_icon']
            if allowed_file(new_icon.filename):
                filename = secure_filename(new_icon.filename)
                new_icon.save(f'app/static/images/icons/{current_user.login}.jpg')
        
        if 'new_font' in request.files:
            new_font = request.files['new_font']
            if allowed_file(new_font.filename):
                filename = secure_filename(new_font.filename)
                new_font.save(f'app/static/images/fonts/{current_user.login}.jpg')

        params = {
            'name'         : name,
            'handleCFORCE' : handleCFORCE,
            'handleTIMUS'  : handleTIMUS,
            'handleINFORM' : handleINFORM,
            'status'       : status,
            'vk_url'       : vk_url,
            'about'        : about
        }

        update = Users.query.filter_by(login = current_user.login).first()
        update.set_params(params)

        if password != '' or confirm_password != '':
            if len(password) < 2:
                flash('Пароль слишком короткий', 'danger')
                return render_template('settings.html')

            elif password != confirm_password:
                flash('Пароли не совпадают', 'danger')
                return render_template('settings.html')
            
            else:
                update.set_password(hashlib.sha224(password.encode('utf-8')).hexdigest())
                flash('Пароль обновлен', 'success')


        db.session.add(update)
        db.session.commit()
        flash('Успешно', 'success')

        return redirect(url_for('profile', login = current_user.login))
    
    return render_template('settings.html' , get_rating = get_rating)