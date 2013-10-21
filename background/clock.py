from rq import Queue
from worker import conn
from apscheduler.scheduler import Scheduler
from tasks import count_words_at_url

q = Queue(connection=conn)
sched = Scheduler()

@sched.interval_schedule(minutes=3)
def timed_job():
    result = q.enqueue(count_words_at_url, 'http://heroku.com')

sched.start()

while True:
    pass

