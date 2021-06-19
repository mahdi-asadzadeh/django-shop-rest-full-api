from celery import shared_task
from .utils import (
    send_register_email, 
    send_reset_password_email,
    send_change_email
)


@shared_task(ignore_result=True)
def task_send_register_email(id, email, username, first_name, last_name):
    send_register_email(id, email, username, first_name, last_name)

@shared_task(ignore_result=True)
def task_send_reset_password_email(id, email, username, first_name, last_name):
    send_reset_password_email(id, email, username, first_name, last_name)

@shared_task(ignore_result=True)
def task_send_change_email(id, email, username, first_name, last_name):
    send_change_email(id, email, username, first_name, last_name)
