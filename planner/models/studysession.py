from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import ValidationError
from datetime import timedelta
from .chapter import Chapter


class StudySession(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    date = models.DateField()
    time_spent = models.DurationField(default=timedelta(0))
    pages_done = models.IntegerField(default=0)
    slides_done = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.chapter.course.pk})
    

    def clean(self):
        if self.time_spent < timedelta(0):
            raise ValidationError({'time_spent': 'Time spent cannot be negative.'})

        # Initialize variables
        remaining_pages = self.chapter.get_remaining_pages() or 0
        remaining_slides = self.chapter.get_remaining_slides() or 0

        if self.pk:
            original = StudySession.objects.get(pk=self.pk)
            remaining_pages += original.pages_done
            remaining_slides += original.slides_done

        # Check if pages_done and slides_done are greater than remaining values
        if self.pages_done > remaining_pages:
            raise ValidationError({'pages_done': 'Pages done cannot be greater than the remaining pages in the chapter.'})
        if self.slides_done > remaining_slides:
            raise ValidationError({'slides_done': 'Slides done cannot be greater than the remaining slides in the chapter.'})


    
    def save(self, *args, **kwargs):
        print("save is called")
        if self.date is None:
            self.date = timezone.now()
        self.full_clean()
        if self.pk:
            original = StudySession.objects.get(pk=self.pk)
            self.chapter.time_spent += self.time_spent - original.time_spent
            self.chapter.pages_completed += self.pages_done - original.pages_done
            self.chapter.slides_completed += self.slides_done - original.slides_done
            print(self.chapter.time_spent) 
            print(original.time_spent)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            self.chapter.add_studysession(self)
        
    def delete(self, *args, **kwargs):
        self.chapter.delete_studysession(self)
        super().delete(*args, **kwargs)