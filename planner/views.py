from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Document, Chapter, Task, Deadline, Milestone


def home(request):
    if not request.user.is_authenticated:
        # todo - make a welcome page
        return redirect('login')
    
    context = {
        'documents': Document.objects.filter(user=request.user)
    }
    return render(request, 'planner/home.html', context)

def planning(request):
    context = {
    }
    return render(request, 'planner/home.html', context)

