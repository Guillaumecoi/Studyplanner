from django.urls import path
from .views.course_views import *
from .views.chapter_views import *
from .views.studysession_views import *


course_urlpatterns = [
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/new/', CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
]

chapter_urlpatterns = [
    path('chapter/<int:pk>/', ChapterDetailView.as_view(), name='chapter-detail'),
    path('course/<int:parent_course_id>/chapter/new/', ChapterCreateView.as_view(), name='chapter-create'),
    path('chapter/<int:pk>/update/', ChapterUpdateView.as_view(), name='chapter-update'),
    path('chapter/<int:pk>/delete/', delete_chapter, name='delete_chapter'),
    path('chapter/<int:pk>/complete', toggle_chapter_completion, name='chapter-complete'),
    path('course/<int:parent_course_id>/chapter/', get_chapters, name='get_chapters'),
]

study_session_urlpatterns = [
    path('chapter/<int:parent_chapter_id>/studysession/', get_studysessions, name='studysession-list'),
    path('chapter/<int:parent_chapter_id>/studysession/new/', StudySessionCreateView.as_view(), name='studysession-create'),
    path('studysession/<int:pk>/update/', StudySessionUpdateView.as_view(), name='studysession-update'),
    path('studysession/<int:pk>/delete/', delete_studysession, name='studysession-delete'),
]

    

urlpatterns = [
    path('', CourseListView.as_view(), name='planner-home'),
] + course_urlpatterns + chapter_urlpatterns + study_session_urlpatterns
