import pickle
from datetime import datetime
import redis
import rq
from flask import current_app
from flask_sqlalchemy_session import current_session
from sqlalchemy import String, Column, Float, Integer, DateTime

from app import Base


class StatusEnum(object):
    PENDING = 0
    RUN = 1
    COMPLETE = 2

    @classmethod
    def state_to_str(cls, state):
        if state == cls.PENDING:
            return 'In Queue'
        elif state == cls.RUN:
            return 'Run'
        elif state == cls.COMPLETE:
            return 'Completed'
        return 'Not defined'


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String(36), primary_key=True)
    process_name = Column(String(10), nullable=True)
    create_time = Column(DateTime(6), default=datetime.utcnow, nullable=False)
    start_time = Column(DateTime(6), nullable=True)
    exec_time = Column(Float, nullable=True)
    status = Column(Integer, default=StatusEnum.PENDING)

    def get_state(self):
        return StatusEnum.state_to_str(self.status)

    def get_job(self):
        try:
            job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return job

    @staticmethod
    def update_by_job(job):
        task = current_session.query(Task).get(job.get_id())
        job_dict = job.to_dict()
        job_meta = pickle.loads(job_dict['meta'])
        task.status = job_meta['status']
        task.exec_time = job_meta.get('work_time')
        task.start_time = job_meta.get('start_time')
        task.process_name = job_meta.get('process_name')
        task.save_task()

    def __repr__(self):
        return '<Task {}>'.format(self.id)

    def to_dict(self):
        return {
            'task_id': self.id,
            'status': self.get_state(),
            'process': self.process_name if self.process_name else '-',
            'create_time': self.create_time.strftime('%Y.%m.%d %H:%M:%S.%f'),
            'exec_time': self.exec_time if self.exec_time else '-',
            'start_time': self.start_time.strftime('%Y.%m.%d %H:%M:%S.%f') if self.start_time else '-'
        }

    def save_task(self):
        try:
            current_session.add(self)
            current_session.commit()
        except (Exception, ) as e:
            current_session.rollback()
            raise Exception(e)
        return True
