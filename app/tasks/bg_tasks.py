from email.mime.text import MIMEText
from typing import Callable, TypeVar

from celery import Celery
import smtplib

from app.config import settings

celery = Celery(
    "mailing",
    broker=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
)

T = TypeVar("T")

CeleryTask = Callable[[Callable[..., T]], Callable[..., T]]


@celery.task(type=CeleryTask)
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
