from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta

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
    pages = models.IntegerField(null=True, blank=True)
    pages_completed = models.IntegerField(default=0)
    time_estimated = models.DurationField(default=timedelta(0), null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0))
    slides = models.IntegerField(null=True, blank=True)
    slides_completed = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order',]
        unique_together = ('course', 'parent_chapter', 'order')
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk:
            max_order = Chapter.objects.filter(course=self.course, parent_chapter=self.parent_chapter).aggregate(models.Max('order'))['order__max']
            if max_order is not None:
                self.order = max_order + 1
        self.course.date_modified = timezone.now()
        self.course.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement the order of chapters with a bigger order
        Chapter.objects.filter(course=self.course, parent_chapter=self.parent_chapter, order__gt=self.order).update(order=models.F('order') - 1)
        super().delete(*args, **kwargs)
        
        
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
        self.course.date_modified = timezone.now()
        self.course.save()
        super().save(*args, **kwargs)
    
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
    

    
