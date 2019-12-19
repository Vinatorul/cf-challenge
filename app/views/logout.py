from flask_login import login_required
from app import *

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли', 'success')
    return redirect(url_for('login'))