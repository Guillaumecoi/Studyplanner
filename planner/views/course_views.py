from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from planner.models.course import Course
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'planner/course/course_list.html'
    context_object_name = 'courses'
    paginate_by = 20
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_sort = '-date_modified' 

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
    template_name = 'planner/course/course_addform.html'
    fields = ['title', 'instructor', 'study_points']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    template_name = 'planner/course/course_updateform.html'
    fields = ['title', 'instructor', 'study_points']
    
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
    template_name = 'planner/course/course_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        course = self.get_object()
        if self.request.user == course.user:
            return True
        return False
    
    
class CourseDetailView(UserPassesTestMixin, DetailView):
    model = Course
    template_name = 'planner/course/course_detail.html'
    
    def test_func(self):
        course = self.get_object()
        if self.request.user == course.user:
            return True
        return False