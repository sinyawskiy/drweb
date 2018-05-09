from flask import Blueprint, current_app, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy_session import current_session

from models import Task, StatusEnum

task_api_bp = Blueprint('task_api', __name__, url_prefix='/api')
task_api = Api(task_api_bp)


class TaskApi(Resource):
    def get(self, task_id=None):
        if task_id:
            tasks = current_session.query(Task).filter_by(id=task_id).all()
        else:
            tasks = current_session.query(Task).all()
        return jsonify([task.to_dict() for task in tasks])

    def post(self):
        job = current_app.task_queue.enqueue(current_app.config['DRWEB_TASK'])
        job.meta['status'] = StatusEnum.PENDING
        job.save_meta()
        task = Task()
        task.id = job.get_id()
        task.save_task()
        task_dict = task.to_dict()

        return jsonify(task_dict)


task_api.add_resource(TaskApi, '/tasks/', '/tasks/<string:task_id>/')
