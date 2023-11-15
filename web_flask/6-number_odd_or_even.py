#!/usr/bin/python3
""" Starts a Flask web application listening on 0.0.0.0, port 5000. """
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Root route ("/") displays the message "Hello HBNB!". """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Root route ("/hbnb") displays “HBNB”. """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ Root route ("/c/<text>") displays “C <text>". """
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def python_text(text="is cool"):
    """ Root route ("/python/<text>") displays "Python <text>". """
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ Root route ("/number/<int:n>") displays "<int:n> is a number". """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ Root route ("/number_template/<int:n>") displays an HTML page. """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ Root route ("/number_odd_or_even/<int:n>") displays an HTML page. """
    if n % 2 == 0:
        value = "even"
    else:
        value = "odd"
    return render_template('6-number_odd_or_even.html', n=n, value=value)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
