from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers

from planner.models import Course, Chapter
from planner.views.view_helper_methods import check_user_course_permission
    
class ChapterDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Chapter
    template_name = 'planner/chapter/chapter_detail.html'
    
    def test_func(self):
        chapter = self.get_object()
        if self.request.user == chapter.course.user:
            return True
        return False

class ChapterCreateView(LoginRequiredMixin, CreateView):
    model = Chapter
    template_name = 'planner/chapter/chapter_addform.html'
    fields = ['title', 'time_estimated', 'pages', 'slides']
    
    def dispatch(self, request, *args, **kwargs):
        response = check_user_course_permission(request, kwargs.get('parent_course_id'))
        if response:
            return response
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        parent_course_id = self.kwargs.get('parent_course_id')
        course = get_object_or_404(Course, id=parent_course_id)
        if course.user != self.request.user:
            messages.error(self.request, "You do not have permission for this course.")
            return HttpResponseRedirect(reverse_lazy('your-error-view-name'))

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
    
class ChapterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chapter
    template_name = 'planner/chapter/chapter_confirm_delete.html'
    
    def test_func(self):
        chapter = self.get_object()
        if self.request.user == chapter.course.user:
            return True
        return False
    
    def get_success_url(self) -> str:
        chapter = self.get_object()
        return reverse('course-detail', args=[str(chapter.course.id)])

class ChapterCompleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chapter
    fields = []
    
    def test_func(self):
        chapter = self.get_object()
        if self.request.user == chapter.course.user:
            return True
        return False
    
    def post(self, request, *args, **kwargs):
        chapter = self.get_object()       
        # Change the chapter
        if chapter.completed == False:
            chapter.complete()
        else:
            chapter.uncomplete()
        chapter.save()
        
        # Return a JSON response
        return JsonResponse({'status': 'success'})


def get_chapters(request, parent_course_id):
    # Get the course
    course = get_object_or_404(Course, id=parent_course_id)

    # Check if the course belongs to the current user
    if request.user != course.user:
        return JsonResponse({'error': 'You do not have permission to view this course'}, status=403)

    # Get the chapters for the course
    chapters = Chapter.objects.filter(course=parent_course_id).order_by('order')

    # Serialize the chapters to JSON and return them
    chapter_list = serializers.serialize('json', chapters)
    return JsonResponse({'chapters': chapter_list})