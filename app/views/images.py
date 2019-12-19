from models.users import *
from flask import current_app
from app import *
import time



@app.route('/user_icon', methods = ['GET'])
def user_icon():    
    login = request.args.get('login')
    try:        
        with current_app.open_resource(f'static/images/icons/{login}.jpg') as img:
            img.close()
        return redirect(url_for('static', filename = f'images/icons/{login}.jpg'))
    except:
        return redirect(url_for('static', filename = 'images/defaults/default_icon.jpg'))

    
    
    
@app.route('/user_font', methods = ['GET', 'POST'])
def user_font():
    login = request.args.get('login')
    try:        
        with current_app.open_resource(f'static/images/fonts/{login}.jpg') as img:
            img.close()
        return redirect(url_for('static', filename = f'images/fonts/{login}.jpg'))
    except:
        return redirect(url_for('static', filename = f'images/defaults/default_font.jpg'))