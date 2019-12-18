from contests_parse import Parsing
from secret import group_id
from models import *
from app import *

@app.route(f'/contest/<int:id>', methods=['GET', 'POST'])
def contest(id):
    try:
        return render_template('contest.html', 
                                id = id, 
                                problems = Parsing(id).get_problems(), 
                                results = Parsing(id).get_solutions(), 
                                group_id = group_id)
    except:
        pass
        #return redirect(url_for('p404'))