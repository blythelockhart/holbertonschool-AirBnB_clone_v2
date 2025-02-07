#!/usr/bin/python3
"""
Starts a Flask web application listening on 0.0.0.0, port 5000.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Displays a list of states sorted by name.
    """
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)

    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """
    Close the current SQLAlchemy Session.
    """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
