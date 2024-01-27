from django.http import HttpResponse
from django.shortcuts import render
from mainapp.tasks import test_func

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