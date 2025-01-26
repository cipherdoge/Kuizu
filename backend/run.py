from app.routes import api
from app.models import db
from flask_cors import CORS
from app import create_app
from celery import Celery
from celery.schedules import crontab
import requests
app = create_app()
CORS(app)


# Flask-Caching Configuration
app.config.update({
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",  # If using Docker, change this to "127.0.0.1" or the correct Redis IP
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_DEFAULT_TIMEOUT": 300
})

# Celery Configuration
app.config.update({
    "broker_url": "redis://localhost:6379/0",  # Redis for message broker
    "result_backend": "redis://localhost:6379/0",
    "timezone": "Asia/Kolkata",  # Replace with your time zone
    "enable_utc": False  # Disable UTC if you're using a local time zone
})



def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

@celery.task
def send_daily_reminders(method, users):
    print(users,"reached sdr")
    for user in users:
        if method == "gchat":
            requests.post(user["webhook_url"], json={"text": f"Hi {user['name']}, don't forget to take your daily quiz!"})
        elif method == "sms":
            # Use Twilio or another SMS provider here
            pass
        elif method == "email":
            # Use SMTP here
            pass

# Celery Beat Example (Schedule Task)
celery.conf.beat_schedule = {
    "send-reminders-every-day": {
        "task": "run.send_daily_reminders",
        "schedule": crontab(minute="*"),  # Adjust time
        "args": ("gchat", [{"name": "Vivi", "webhook_url": "https://chat.googleapis.com/v1/spaces/AAAAzVxtSfs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=apnWZYEA4lf78HHwfFBZYTl0aDCdnxJtKHpeHiYs4C4"}]),  
    },
}



if __name__ == '__main__':
    app.run(port=5000,debug=True)

