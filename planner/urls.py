from django.urls import path
from .views.course_views import *
from planner.views import views


courseurlpatterns = [
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/new/', CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
]
    

urlpatterns = [
    path('', CourseListView.as_view(), name='planner-home'),
] + courseurlpatterns
