from flask import Flask
from flask_bootstrap import Bootstrap
import config
import os
import app
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name,backend=config.CELERY_RESULT_BACKEND, broker=config.CELERY_BROKER_URL)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery

app = Flask(__name__)

# Configurations
app.config.from_object('config')

#celery
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)


#Bootstrap
bootstrap = Bootstrap(app)

#celery
celery = make_celery(app)
print("celery made")
#blueprints
from app.extractor.views import extractor
app.register_blueprint(extractor)



