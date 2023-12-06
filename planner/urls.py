from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='planner-home'),
    path('planning/', views.planning, name='planning'),
]