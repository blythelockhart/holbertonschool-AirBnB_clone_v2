#!/usr/bin/python3
"""
Starts a Flask web application.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_id(id=None):
    """
    Display a page with the list of City objects linked to a State.
    """
    if id != None:
        states = storage.get("State", id)
    else:
        states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    
    return render_template('9-states.html', states=states, id=id)


@app.teardown_appcontext
def teardown(exception):
    """
    Close the current SQLAlchemy Session.
    """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
