from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from config import config_dic
from redis import Redis
import rq
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_task_api(app):
    try:
        from api_1_0 import task_api_bp

        app.register_blueprint(task_api_bp)
    except (ImportError,) as msg:
        pass


def create_app(config_name='development'):
    app = Flask(__name__)
    setup = config_dic.get(config_name)

    if setup:
        app.config.from_object(setup)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db_session = flask_scoped_session(session_factory)
    db_session.init_app(app)

    Base = declarative_base()
    Base.query = db_session.query_property()

    def do_setup():
        Base.metadata.create_all(bind=engine)

    do_setup()
    create_task_api(app)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('drweb-tasks', connection=app.redis)

    return {'app': app, 'db_session': db_session, 'Base': Base}
