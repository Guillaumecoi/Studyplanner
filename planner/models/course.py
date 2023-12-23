from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructor = models.CharField(null=True, blank=True , max_length=100)
    description = models.TextField(null=True, blank=True)
    study_points = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.completed and not self.date_completed:
            self.date_completed = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})
    
    def modified(self):
        self.date_modified = timezone.now()
        self.save()