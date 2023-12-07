import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Document, Chapter, Task, Deadline, Milestone


def home(request):
    if not request.user.is_authenticated:
        # todo - make a welcome page
        return redirect('login')
    
    context = {
        'documents': Document.objects.filter(user=request.user)
    }
    return render(request, 'planner/home.html', context)

class DocumentListView(ListView):
    model = Document
    template_name = 'planner/home.html'
    context_object_name = 'documents'
    ordering = ['-date_added']
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
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
            form.instance.date_completed = datetime.datetime.now()
        return super().form_valid(form)
    
    def test_func(self):
        document = self.get_object()
        if self.request.user == document.user:
            return True
        return False
    
class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    success_url = '/'
    
    def test_func(self):
        document = self.get_object()
        if self.request.user == document.user:
            return True
        return False

