from email.mime.text import MIMEText
from redis import asyncio as aioredis
from celery import Celery
from celery.schedules import crontab
import smtplib

from app.config import settings

celery = Celery(
    "mailing",
    broker=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
)

celery.conf.beat_schedule = {
    "reset_daily_matches_counter": {
        "task": "reset_daily_matches_counter",
        "schedule": crontab(hour=0, minute=0),
    },
}


@celery.task
def send_match_notification(
        email: str,
        matched_name: str,
        matched_email: str
) -> None:

    message_text = (
        f"Вы понравились {matched_name}! Почта участника: {matched_email}"
    )
    message = MIMEText(message_text)
    message['Subject'] = "Взаимная симпатия!"
    message['From'] = settings.SMTP_USER
    message['To'] = email

    with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, email, message.as_string())


@celery.task
async def reset_daily_matches_counter() -> None:
    redis = aioredis.from_url(settings.REDIS_URL)
    keys = await redis.keys("matches_count:*")
    for key in keys:
        await redis.delete(key)
