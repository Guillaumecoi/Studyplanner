from django.utils import timezone
from django.db import models
from datetime import timedelta
from .course import Course
from .chapter import Chapter


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
        self.chapter.course.modified()
        self.date = timezone.now().date()
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.chapter.time_spent -= self.time_spent
        self.chapter.save()
        super().delete(*args, **kwargs)