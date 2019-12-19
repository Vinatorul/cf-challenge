from models.contests import Contests
from models.users import Users
from app import *

@app.route('/deleteContest', methods = ['GET'])
def deleteContest():
    if current_user.role == "User":
        return redirect(url_for('index'))
    id = request.args.get('id')
    try:
        db.session.delete(Contests.query.filter_by(id=id).first())
        db.session.commit()
        return redirect(url_for('index'))
    except:
        flash('Ошибка', 'danger')
        return redirect(url_for('index'))
    
    
@app.route('/deleteUser', methods = ['GET'])
def deleteUser():
    if current_user.role == "User":
        return redirect(url_for('index'))
    id = request.args.get('id')
    try:
        db.session.delete(Users.query.filter_by(id=id).first())
        db.session.commit()
        return redirect(url_for('users'))
    except:
        flash('Ошибка', 'danger')
        return redirect(url_for('users'))
    
    
@app.route('/addAdmin', methods = ['GET'])
def addAdmin():
    if current_user.role == "User":
        return redirect(url_for('index'))
    login = request.args.get('login')
    try:
        admin = Users.query.filter_by(login=login).first()
        admin.role = 'Admin'
        db.session.add(admin)
        db.session.commit()
        flash('Успешно', 'success')
        return redirect(url_for('profile', login = login))
    except:
        flash('Ошибка', 'danger')
        return redirect(url_for('profile', login = login))
    
    
@app.route('/deleteAdmin', methods = ['GET'])
def deleteAdmin():
    if current_user.role == "User":
        return redirect(url_for('index'))
    login = request.args.get('login')
    try:
        admin = Users.query.filter_by(login=login).first()
        admin.role = 'User'
        db.session.add(admin)
        db.session.commit()
        flash('Успешно', 'success')
        return redirect(url_for('profile', login = login))
    except:
        flash('Ошибка', 'danger')
        return redirect(url_for('profile', login = login))