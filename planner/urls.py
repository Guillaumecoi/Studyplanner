from django.urls import path
from .views.course_views import *
from .views.chapter_views import *
from .views.studysession_views import *
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
    path('course/<int:parent_course_id>/chapter/<int:pk>/complete/', ChapterCompleteView.as_view(), name='chapter-complete'),
    path('api/course/<int:parent_course_id>/chapters/', get_chapters, name='get_chapters'),
]

study_session_urlpatterns = [
    path('course/<int:parent_course_id>/chapter/<int:parent_chapter_id>/session/new/', StudySessionCreateView.as_view(), name='studysession-create'),
    path('course/<int:parent_course_id>/chapter/<int:parent_chapter_id>/session/<int:pk>/update/', StudySessionUpdateView.as_view(), name='studysession-update'),
    path('course/<int:parent_course_id>/chapter/<int:parent_chapter_id>/session/<int:pk>/delete/', StudySessionDeleteView.as_view(), name='studysession-delete'),
]

    

urlpatterns = [
    path('', CourseListView.as_view(), name='planner-home'),
] + course_urlpatterns + chapter_urlpatterns + study_session_urlpatterns
