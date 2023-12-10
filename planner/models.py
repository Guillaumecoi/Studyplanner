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
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})
    
    
class Chapter(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    parent_chapter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=0)
    content = models.TextField()
    pages = models.IntegerField(default=0)
    guessed_time = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order',]
        unique_together = ('course', 'parent_chapter', 'order')
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.course.date_modified = timezone.now()
        self.course.save()
        super().save(*args, **kwargs)
        
class Task(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    time_estimated = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order',]
        
    def __str__(self):
        return self.title
    
class Deadline(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
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
    

    
