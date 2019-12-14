from models.users import *
from app import *

@app.route('/profile/<handle>', methods = ['GET', 'POST'])
def profile(handle):

    
    if bool(Users.query.filter_by(handle = handle).first()):
        user_obj = Users.query.filter_by(handle = handle).first()
        return render_template('profile.html', user_obj = user_obj)
    else:
        return render_template('profile.html', user_obj = '', handle = handle)
