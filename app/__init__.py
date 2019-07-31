from flask import Flask
from app.extractor.views import extract, api
from flask_bootstrap import Bootstrap
from celery import Celery
import config
import os


def make_celery(app):
    celery = Celery(app.import_name, broker=config.CELERY_BROKER)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery

# Import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy


# Define the WSGI application object
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
#db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)

# Register blueprint(s)

app.register_blueprint(extract)
app.register_blueprint(api)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()

# create celery object
celery = make_celery(app)
