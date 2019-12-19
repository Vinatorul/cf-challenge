from app import *

@app.route('/404')
def p404():
    return render_template('p404.html')