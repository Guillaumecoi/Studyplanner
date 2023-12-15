from django.urls import path
from .views.course_views import *
from .views.chapter_views import *
from planner.views import views


course_urlpatterns = [
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/new/', CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
]

chapter_urlpatterns = [
    path('course/<int:parent_course_id>/chapter/<int:pk>/', ChapterDetailView.as_view(), name='chapter-detail'),
    path('course/<int:parent_course_id>/chapter/new/', ChapterCreateView.as_view(), name='chapter-create'),
    path('course/<int:parent_course_id>/chapter/<int:pk>/update/', ChapterUpdateView.as_view(), name='chapter-update'),
    path('course/<int:parent_course_id>/chapter/<int:pk>/delete/', ChapterDeleteView.as_view(), name='chapter-delete'),
]
    

urlpatterns = [
    path('', CourseListView.as_view(), name='planner-home'),
] + course_urlpatterns + chapter_urlpatterns
