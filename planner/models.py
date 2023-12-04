from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    study_points = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    
class Chapter(models.Model):
    title = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    parent_chapter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=0)
    content = models.TextField()
    pages = models.IntegerField(default=0)
    guessed_time = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order',]
        
    def __str__(self):
        return self.title
        
class Task(models.Model):
    title = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
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
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class Milestone(models.Model):
    title = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    chapters = models.ManyToManyField(Chapter)
    tasks = models.ManyToManyField(Task)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    

    
