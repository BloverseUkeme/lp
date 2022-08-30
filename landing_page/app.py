from flask import Flask
from landing_page.views import lpage_bp
from celery import Celery
from decouple import config as env_config

from landing_page.extensions import oauth


# MAIL_PASSWORD= env_config("MAIL_PASSWORD")



CELERY_TASK_LIST = [
    "landing_page.tasks.lpage",
]



def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.logger.setLevel('DEBUG')
    app.register_blueprint(lpage_bp)
    
    app.secret_key = "lpage"

    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_USERNAME'] = 'no-reply@bloverse.com'
    # app.config['MAIL_PASSWORD'] = MAIL_PASSWORD 



    extensions(app)

    return app




# def create_celery_app(app=None):
#     """
#     Create a new Celery object and tie together the Celery config to the app's
#     config. Wrap all tasks in the context of the application.

#     :param app: Flask app
#     :return: Celery app
#     """
#     app = app or create_app()

#     celery = Celery(app.import_name, 
#                     broker=app.config['CELERY_BROKER_URL'],
#                     backend_url=app.config["CELERY_RESULT_BACKEND"],
#                     include=CELERY_TASK_LIST)

#     celery.conf.update(app.config)

#     TaskBase = celery.Task

#     class ContextTask(TaskBase):
#         abstract = True

#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)

#     celery.Task = ContextTask
#     return celery



def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    oauth.init_app(app)
    # mail.init_app(app)
    
    return None
