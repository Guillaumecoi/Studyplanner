from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView
from planner.models.course import Course
from planner.models.chapter import Chapter
from planner.models.studysession import StudySession
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


    
class StudySessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = StudySession
    template_name = 'planner/studysession/studysession_createform.html'
    fields = ['time_spent', 'pages_done', 'slides_done']
    
    def test_func(self):
        parent_chapter_id = self.kwargs.get('parent_chapter_id')
        chapter = get_object_or_404(Chapter, pk=parent_chapter_id)
        return chapter.course.has_access(self.request.user)
    
    def post(self, request, *args, **kwargs):
        self.object = None  # This is usually None in CreateView
        form = self.get_form()
        chapter = get_object_or_404(Chapter, pk=self.kwargs.get('parent_chapter_id'))
        form.instance.chapter = chapter

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)  
         
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapter'] = get_object_or_404(Chapter, pk=self.kwargs.get('parent_chapter_id'))
        context['remaining_pages'] = context['chapter'].get_remaining_pages()
        context['remaining_slides'] = context['chapter'].get_remaining_slides()
        return context
        
    
class StudySessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudySession
    template_name = 'planner/studysession/studysession_updateform.html'
    fields = ['time_spent', 'pages_done', 'slides_done']
    
    def test_func(self):
        studysession = self.get_object()
        return studysession.chapter.course.has_access(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        studySession = self.get_object()
        context['chapter'] = studySession.chapter
        context['remaining_pages'] = context['chapter'].get_remaining_pages() + studySession.pages_done
        context['remaining_slides'] = context['chapter'].get_remaining_slides() + studySession.slides_done
        return context
    
    
@login_required
@require_http_methods(["DELETE"])
def delete_studysession(request, pk):
    studysession = get_object_or_404(StudySession, pk=pk)

    # Check if the course belongs to the current user
    if not studysession.chapter.course.has_access(request.user):
        raise PermissionDenied('You do not have permission to modify this chapter')

    try:
        studysession.delete()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'error'}, status=500)

@login_required
@require_GET
def get_studysessions(request, parent_chapter_id):
    # Get the chapter
    chapter = get_object_or_404(Chapter, id=parent_chapter_id)

    # Check if the course belongs to the current user
    if not chapter.course.has_access(request.user):
        raise PermissionDenied('You do not have permission to view this course')

    # Get the study sessions for the chapter
    studysessions = StudySession.objects.filter(chapter=chapter)

    # Serialize the study sessions to JSON and return them
    studysession_list = serializers.serialize('json', studysessions)
    return JsonResponse({'studysessions': studysession_list})