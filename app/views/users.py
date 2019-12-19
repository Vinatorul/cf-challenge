from contests_parse import *
from models.users import Users
from models import *
from app import *

@app.route('/users')
def users():
    
    users = Users.query.order_by(Users.login).all()  
    return render_template('users.html', users = users, get_rating = get_rating)