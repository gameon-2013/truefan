# path fix
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'truefan.settings'

import django_rq

from apscheduler.scheduler import Scheduler
from twyauth.tasks import analyze_all_profile_tweets

q = django_rq.get_queue()
sched = Scheduler()

@sched.interval_schedule(minutes=60)
def timed_job():
    q.enqueue_call(func=analyze_all_profile_tweets, result_ttl=0)

sched.start()

while True:
    pass

