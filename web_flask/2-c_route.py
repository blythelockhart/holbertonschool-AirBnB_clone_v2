#!/usr/bin/python3
"""
Starts a Flask web application listening on 0.0.0.0, port 5000.
Root route ("/") displays the message "Hello HBNB!".
Root route ("/hbnb") displays “HBNB”.
Root route ("/c/<text>") displays “C ” and the value of the text variable.
"""

fromm flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    # Replace underscores with spaces in the text variable
    formatted_text = text.replace('_', ' ')
    return 'C {}'.format(formatted_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
