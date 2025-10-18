from celery import Celery
import os
import time

BROKER = os.getenv("CELERY_BROKER_URL", "amqp://rabbit:rabbit@rabbitmq:5672//")
BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery("tasks", broker=BROKER, backend=BACKEND)

@celery_app.task(name="send_issue_notification")
def send_issue_notification(issue_id: int, summary: str):
    # Placeholder: in production integrate with SMTP or external service
    print(f"[TASK] Notify about issue {issue_id}: {summary}")
    time.sleep(1)
    return True
