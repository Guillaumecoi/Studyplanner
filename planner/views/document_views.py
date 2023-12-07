from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from planner.models import Document


class DocumentListView(ListView):
    model = Document
    template_name = 'planner/home.html'
    context_object_name = 'documents'
    paginate_by = 5
    
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
    
class DocumentDetailView(UserPassesTestMixin, DetailView):
    model = Document
    
    def test_func(self):
        document = self.get_object()
        if self.request.user == document.user:
            return True
        return False

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'instructor', 'description', 'study_points']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DocumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    fields = ['title', 'instructor', 'description', 'study_points', 'completed']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.completed:
            form.instance.date_completed = timezone.now()
        return super().form_valid(form)
    
    def test_func(self):
        document = self.get_object()
        if self.request.user == document.user:
            return True
        return False
    
class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    success_url = ''
    
    def test_func(self):
        document = self.get_object()
        if self.request.user == document.user:
            return True
        return False