from django import forms
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from planner.models import Course, Chapter

class UserCoursePermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        parent_course_id = kwargs.get('parent_course_id')
        course = get_object_or_404(Course, id=parent_course_id)
        if not request.user == course.user:
            # Return a 403 Forbidden response
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

class ChapterCreateView(LoginRequiredMixin, UserCoursePermissionMixin, CreateView):
    model = Chapter
    template_name = 'planner/chapter/chapter_addform.html'
    fields = ['title', 'time_estimated', 'pages', 'slides']
    
    def form_valid(self, form):
        parent_course_id = self.kwargs.get('parent_course_id')
        course = get_object_or_404(Course, id=parent_course_id)
        if course.user != self.request.user:
            messages.error(self.request, "You do not have permission for this course.")
            return HttpResponseRedirect(reverse_lazy('your-error-view-name'))  # Adjust the redirection as needed

        form.instance.course = course
        return super().form_valid(form)
    
class ChapterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chapter
    template_name = 'planner/chapter/chapter_updateform.html'
    fields = ['title', 'time_estimated', 'pages', 'slides']
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def test_func(self):
        chapter = self.get_object()
        if self.request.user == chapter.course.user:
            return True
        return False
