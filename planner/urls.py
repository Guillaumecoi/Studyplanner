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
    path('chapter/new/<int:parent_course>/<int:parent_chapter>/', ChapterCreateView.as_view(), name='chapter-create'),
]
    

urlpatterns = [
    path('', CourseListView.as_view(), name='planner-home'),
] + course_urlpatterns + chapter_urlpatterns
