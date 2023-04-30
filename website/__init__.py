from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_executor import Executor


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'reallysecretcode'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
