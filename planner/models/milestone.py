from django.utils import timezone
from django.db import models
from datetime import timedelta
from .course import Course
from .chapter import Chapter
from .task import Task

    
class Milestone(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapters = models.ManyToManyField(Chapter)
    tasks = models.ManyToManyField(Task)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.course.modified()
        super().save(*args, **kwargs)