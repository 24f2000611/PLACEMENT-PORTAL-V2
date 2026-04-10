from celery import Celery
from celery.schedules import crontab
from Backend.task import *



def make_celery(app):
    celery_app = Celery(
        app.import_name,
        broker= 'redis://localhost:6379/0',
        backend= 'redis://localhost:6379/0',
        include= ['Backend.task']
    )
    celery_app.conf.update(app.config)
    celery_app.conf.timezone = 'Asia/Kolkata'

    class ContextTask(celery_app.Task):
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return self.run(*args ,**kwargs)
            
    celery_app.Task = ContextTask


    celery_app.conf.beat_schedule= {
        'daily-interview-reminders':{
            'task':"Backend.task.send_interview_reminders",
            'schedule': crontab(minute = '*'),

        },
        'monthly-placement-reports':{
            'task':'Backend.task.generate_monthly_reports',
            'schedule':crontab(minute='*')
        }
    }
    return celery_app