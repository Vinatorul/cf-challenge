from models.users import *
from contests_parse import get_rating
from app import *

@app.route('/profile/<login>', methods = ['GET', 'POST'])
def profile(login):

    if bool(Users.query.filter_by(login = login).first()):
        user_obj = Users.query.filter_by(login = login).first()
        return render_template('profile.html', user_obj = user_obj, get_rating = get_rating)
    
    elif bool(Users.query.filter_by(handleCFORCE = login).first()):
        user_obj = Users.query.filter_by(handleCFORCE = login).first()
        return render_template('profile.html', user_obj = user_obj, get_rating = get_rating)
    
    elif get_rating([login]) != None:
        return render_template('profile.html', user_obj = '', handleCFORCE = login , get_rating = get_rating)
    
    else:
        return redirect(url_for('p404'))

        
