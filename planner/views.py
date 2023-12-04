from django.shortcuts import render
from django.http import HttpResponse
from .models import Document, Chapter, Task, Deadline, Milestone


def home(request):
    context = {
        'documents': Document.objects.all()
    }
    return render(request, 'planner/home.html', context)

def planning(request):
    context = {
    }
    return render(request, 'planner/home.html', context)

