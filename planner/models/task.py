from django.utils import timezone
from django.db import models
from datetime import timedelta
from .course import Course
from .chapter import Chapter

class Task(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=0)
    time_estimated = models.DurationField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0))
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order',]
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.course.modified()
        super().save(*args, **kwargs)