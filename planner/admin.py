from django.contrib import admin
from .models.course import Course
from .models.chapter import Chapter

admin.site.register(Course)
admin.site.register(Chapter)

