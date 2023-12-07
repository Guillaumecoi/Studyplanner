from django.urls import path
from .views import DocumentListView, DocumentDetailView, DocumentCreateView, DocumentUpdateView, DocumentDeleteView
from . import views


documenturlpatterns = [
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('document/new/', DocumentCreateView.as_view(), name='document-create'),
    path('document/<int:pk>/update/', DocumentUpdateView.as_view(), name='document-update'),
    path('document/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
]
    

urlpatterns = [
    path('', DocumentListView.as_view(), name='planner-home'),
] + documenturlpatterns
