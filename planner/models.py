from collections.abc import Iterable
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
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
    
    def save(self, *args, **kwargs):
        if self.completed and not self.date_completed:
            self.date_completed = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})
    
    
class Chapter(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    parent_chapter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=1)
    content = models.TextField()
    pages = models.IntegerField(null=True, blank=True)
    pages_completed = models.IntegerField(default=0)
    time_estimated = models.DurationField(default=timedelta(0), null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0), null=True, blank=True)
    slides = models.IntegerField(null=True, blank=True)
    slides_completed = models.IntegerField(default=0)
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order',]
        unique_together = ('course', 'parent_chapter', 'order')
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # auto increment order
        if not self.pk:
            max_order = Chapter.objects.filter(course=self.course, parent_chapter=self.parent_chapter).aggregate(models.Max('order'))['order__max']
            if max_order is not None:
                self.order = max_order + 1
                
        # Update the course's date_modified
        update_modifieddate(self.course)
        
        # If the chapter is marked as completed, call the complete method before saving.
        if self.completed:
            self.complete()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement the order of chapters with a bigger order
        Chapter.objects.filter(course=self.course, parent_chapter=self.parent_chapter, order__gt=self.order).update(order=models.F('order') - 1)
        super().delete(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.course.pk})
    
    def complete(self):
        if not self.date_completed or self.date_completed > timezone.now():
            self.date_completed = timezone.now().date()
        self.pages_completed = self.pages
        self.slides_completed = self.slides
        self.progress = 100
        
    
class StudySession(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    date = models.DateField()
    time_spent = models.DurationField(default=timedelta(0))
    pages_done = models.IntegerField(default=0)
    slides_done = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.chapter.title} - {self.date}"
    
    def save(self, *args, **kwargs):
        self.chapter.time_spent += self.time_spent
        self.chapter.save()
        update_modifieddate(self.chapter.course)
        self.date = timezone.now().date()
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.chapter.time_spent -= self.time_spent
        self.chapter.save()
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
        update_modifieddate(self.course)
        super().save(*args, **kwargs)
    
class Deadline(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        update_modifieddate(self.course)
        super().save(*args, **kwargs)
    
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
        update_modifieddate(self.course)
        super().save(*args, **kwargs)
    
    
def update_modifieddate(course):
    course.date_modified = timezone.now()
    course.save()
    

    
