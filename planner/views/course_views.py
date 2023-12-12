from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from planner.models import Course, Chapter

class CourseListView(ListView):
    model = Course
    template_name = 'planner/course_list.html'
    context_object_name = 'courses'
    paginate_by = 20
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_sort = '-date_modified'  # Default sort order

    def get_queryset(self):
        self.current_sort = self.request.GET.get('sort', '-date_modified')
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by(self.current_sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.current_sort
        return context
        
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'instructor', 'description', 'study_points']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'instructor', 'description', 'study_points', 'completed']
    
    def form_valid(self, form):
        if form.instance.completed:
            form.instance.date_completed = timezone.now()
        return super().form_valid(form)
    
    def test_func(self):
        course = self.get_object()
        if self.request.user == course.user:
            return True
        return False
    
class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = '/'
    
    def test_func(self):
        course = self.get_object()
        if self.request.user == course.user:
            return True
        return False
    
    
class CourseDetailView(UserPassesTestMixin, DetailView):
    model = Course
    
    def test_func(self):
        course = self.get_object()
        if self.request.user == course.user:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Get chapters related to the course
        chapters = Chapter.objects.filter(course=course).order_by('order')
        context['chapters'] = chapters
        
        return context
