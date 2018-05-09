import contextlib
import time
import rq
from redis import Redis
from create_app import create_app
import multiprocessing
from datetime import datetime

app = create_app(config_name='default')
app_obj = app.get('app')
Base = app.get('Base')
db_session = app.get('db_session')


def process_tasks():
    from models import StatusEnum, Task
    queue = rq.Queue('drweb-tasks', connection=Redis.from_url('redis://'))
    with app_obj.app_context():
        while True:
            job = queue.dequeue()
            if job:
                job.meta['status'] = StatusEnum.RUN
                job.meta['start_time'] = datetime.utcnow()
                job.meta['process_name'] = multiprocessing.current_process().name
                job.save_meta()
                Task.update_by_job(job)
                start_time = time.time()
                queue.run_job(job)
                job.meta['status'] = StatusEnum.COMPLETE
                job.meta['work_time'] = time.time() - start_time
                job.save_meta()
                Task.update_by_job(job)


if __name__ == '__main__':
    for i in range(app_obj.config['PROCESSES_LIMIT']):
        task_process = multiprocessing.Process(target=process_tasks)
        task_process.start()

    app_obj.template_folder = app_obj.config['TEMPLATE_FOLDER']
    app_obj.static_folder = app_obj.config['STATIC_FOLDER']
    app_obj.use_reloader = app_obj.config['USE_RELOADER']
    app_obj.run(port=app_obj.config['PORT'], host=app_obj.config['HOST'], debug=False)
