from flask import Flask
from flask_bootstrap import Bootstrap
import config
import os
from app.extractor.views import extractor

# Import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy

import crochet
crochet.setup()     # initialize crochet

# Define the WSGI application object
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Configurations
app.config.from_object('config')
print("init run")
# Define the database object which is imported
# by modules and controllers
#db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)

# Register blueprint(s)
app.register_blueprint(extractor)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()

# create celery object
#celery = make_celery(app)
