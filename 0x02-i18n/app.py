#!/usr/bin/env python3
""" module's doc str """


from typing import List, Dict, Union, Sequence, Callable, Any
from flask_babel import Babel, gettext
from flask import Flask, render_template, g, request
from datetime import datetime
from pytz import timezone


app = Flask(__name__)
babel = Babel(app, default_locale='en', default_timezone='UTC')


class Config(object):
    """ config for babel """
    LANGUAGES = ['en', "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

users: Dict[int, Dict] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """ gets user """
    id = request.args.get('login_as', None)
    if id:
        try:
            id = int(id)
        except Exception:
            id = None
    return users.get(id)


@app.before_request
def before_request() -> Union[Dict, None]:
    """ execute before each req """
    g.user = get_user()
    if g.user:
        user = g.user
        now = datetime.now()
        # fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        fmt = '%b %d, %Y, %I:%M:%S %p'
        tz = timezone(user.get('timezone'))
        loc_t = tz.localize(datetime.now())
        time = loc_t.strftime(fmt)
        g.time = str(time)
        # print(g.time)


@babel.localeselector
def get_locale() -> Union[str, None]:
    """ override default fet_locale """
    locale = request.args.get('locale', None)
    if locale in Config.LANGUAGES:
        return locale
    user = g.user
    if user:
        return user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> Union[str, None]:
    """ override default get_timezone """
    timezone = request.args.get('timezone', None)
    if timezone:
        return timezone

    # user = g.user
    # if user:
    #     return user.get('timezone')
    return 'UTC'


@app.route('/', strict_slashes=False)
def index() -> str:
    """ root path """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
