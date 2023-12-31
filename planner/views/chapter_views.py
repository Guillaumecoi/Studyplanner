from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.core import serializers

from planner.models.course import Course
from planner.models.chapter import Chapter
    
class ChapterDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Chapter
    template_name = 'planner/chapter/chapter_detail.html'
    
    def test_func(self):
        chapter = self.get_object()
        return chapter.course.has_access(self.request.user)
    
    def get_context_data(self, **kwargs):
        chapter = self.get_object()
        context = super().get_context_data(**kwargs)
        context['time_spent_percentage'] = min((chapter.time_spent / chapter.time_estimated if chapter.time_estimated else 0), 1) * 100  # Time progress cannot be greater than 100
        return context

class ChapterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Chapter
    template_name = 'planner/chapter/chapter_addform.html'
    fields = ['title', 'time_estimated', 'pages', 'slides']

    def test_func(self):
        parent_course_id = self.kwargs.get('parent_course_id')
        course = get_object_or_404(Course, id=parent_course_id)
        return course.has_access(self.request.user)

    def form_valid(self, form):
        parent_course_id = self.kwargs.get('parent_course_id')
        form.instance.course = get_object_or_404(Course, id=parent_course_id)
        return super().form_valid(form)
    
class ChapterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chapter
    template_name = 'planner/chapter/chapter_updateform.html'
    fields = ['title', 'time_estimated', 'pages', 'slides']
    
    def test_func(self):
        chapter = self.get_object()
        return chapter.course.has_access(self.request.user)
    

@login_required
@require_http_methods(["DELETE"])
def delete_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)

    # Check if the course belongs to the current user
    if not chapter.course.has_access(request.user):
        raise PermissionDenied('You do not have permission to modify this chapter')

    try:
        chapter.delete()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'error'}, status=500)


@login_required
@require_POST
def toggle_chapter_completion(request, pk):
    # Get the chapter
    chapter = get_object_or_404(Chapter, pk=pk)

    # Check if the course belongs to the current user
    if not chapter.course.has_access(request.user):
        raise PermissionDenied('You do not have permission to modify this chapter')

    try:
        # Toggle the completion status
        if chapter.completed:
            chapter.uncomplete()
        else:
            chapter.complete()

        # Return a JSON response
        return JsonResponse({'status': 'success', 'completed': chapter.completed})
    except:
        return JsonResponse({'error': 'Chapter is not complete'}, status=400)
    

@login_required
@require_GET
def get_chapters(request, parent_course_id):
    # Get the course
    course = get_object_or_404(Course, id=parent_course_id)

    # Check if the course belongs to the current user
    if not course.has_access(request.user):
        raise PermissionDenied('You do not have permission to view this course')

    # Get the chapters for the course
    chapters = Chapter.objects.filter(course=parent_course_id).order_by('order')

    # Serialize the chapters to JSON and return them
    chapter_list = serializers.serialize('json', chapters)
    return JsonResponse({'chapters': chapter_list})