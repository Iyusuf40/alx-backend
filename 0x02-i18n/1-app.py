#!/usr/bin/env python3
""" module's doc str """


from typing import List, Dict, Union, Sequence, Callable, Any
from flask_babel import Babel
from flask import Flask, render_template


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """ config for babel """
    LANGUAGES = ['en', "fr"]


def get_locale():
    return Config.LANGUAGES


babel.init_app(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def index() -> str:
    """ root path """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
