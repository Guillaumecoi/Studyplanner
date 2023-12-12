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
        parent_course_id = kwargs.get('parent_course')
        course = get_object_or_404(Course, id=parent_course_id)
        if not request.user == course.user:
            # Return a 403 Forbidden response
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

class ChapterCreateView(LoginRequiredMixin, UserCoursePermissionMixin, CreateView):
    model = Chapter
    fields = ['title', 'pages', 'guessed_time']
    
    def get_success_url(self):
        # Redirect to the detail view of the course associated with this chapter
        return reverse('course-detail', kwargs={'pk': self.object.course.pk})

    
    def form_valid(self, form):
        # Retrieve the course and parent chapter using the ID from URL parameters
        parent_course_id = self.kwargs.get('parent_course')
        parent_chapter_id = self.kwargs.get('parent_chapter')

        # Fetch the course and check if it belongs to the user
        course = get_object_or_404(Course, id=parent_course_id)
        if course.user != self.request.user:
            messages.error(self.request, "You do not have permission for this course.")
            return HttpResponseRedirect(reverse_lazy('your-error-view-name'))  # Adjust the redirection as needed

        form.instance.course = course

        # Check if parent chapter is valid and belongs to the same course
        if parent_chapter_id != 0:
            parent_chapter = get_object_or_404(Chapter, id=parent_chapter_id, course=course)
            form.instance.parent_chapter = parent_chapter
        else:
            form.instance.parent_chapter = None

        return super().form_valid(form)

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'pages', 'time_estimated', 'slides']
