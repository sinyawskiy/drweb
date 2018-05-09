import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TEMPLATE_FOLDER = os.getenv('template_folder', os.path.join(PROJECT_ROOT, 'templates'))
    STATIC_FOLDER = os.getenv('static_folder', os.path.join(PROJECT_ROOT, 'static'))
    DEBUG = os.getenv('DEBUG', True)
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 8080)
    USE_RELOADER = os.getenv('USE_RELOADER', False)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://drweb:password@localhost/drweb'
    PROCESSES_LIMIT = 2
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    DRWEB_TASK = 'task.main'

    @staticmethod
    def init_app(app):
        pass


config_dic = {
    'default': Config,
}
