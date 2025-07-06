from datetime import datetime
from django.utils.timezone import now
from .models import UserProfile
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
 
 
from datetime import datetime
import pytz
import time
import threading
from django.utils import timezone
 
 
from accounts.models import UserProfile
 
def my_scheduled_job():
    subscribers = UserProfile.objects.filter(is_subscribed=True)
    for subscriber in subscribers:        
        if now() >= subscriber.subsciption_expires_on:
            subscriber.is_subscribed = False
            subscriber.subscription_status = "freemium"
            subscriber.save()
 
def print_time_until_next_execution(scheduler, job_id):
    while True:
        job = scheduler.get_job(job_id)
        if job and job.next_run_time:
            now = datetime.now(pytz.utc)
            time_left = job.next_run_time - now
            print(f"Time until next execution: {time_left}", end="\r")
        else:
            pass
        time.sleep(1)
 
 
def start_scheduler():
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(my_scheduled_job, IntervalTrigger(hours=12), replace_existing=True, id="daily_task")
    scheduler.start()
 
    print("Scheduler started")
 
    # Start the countdown in a separate thread
    threading.Thread(target=print_time_until_next_execution, args=(scheduler, "daily_task"), daemon=True).start()