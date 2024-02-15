from celery.schedules import crontab
from django.http.response import HttpResponse
from django.shortcuts import render
from .tasks import test_func
from send_mail_app.tasks import send_mail_func
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# Create your views here.
#! READ THE COMMENTS BELOW CAREFULLY.
"""
In this code snippet, the "Done" response is sent immediately after the Celery task test_func is scheduled for execution using the delay() method.

The delay() method in Celery doesn't wait for the task to complete; instead, it queues the task for execution and returns immediately. This means that when the test view is called, it triggers the test_func task and then immediately returns the "Done" response without waiting for test_func to finish executing.

As a result, the "Done" response is sent back to the client as soon as the view is called, regardless of whether the test_func task has finished running or not. The actual execution of test_func happens asynchronously in the background by Celery.
"""

def test(request):
    test_func.delay() #! It calls test_func.delay(). This is using Celery's delayed task execution mechanism. Instead of executing test_func immediately, it schedules it to be executed asynchronously by a Celery worker.
    return HttpResponse("Done")

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 22, minute = 19)
    task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"+"7", task='send_mail_app.tasks.send_mail_func')#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")