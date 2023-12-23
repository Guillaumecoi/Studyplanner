from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from datetime import timedelta
from .course import Course

class Chapter(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    parent_chapter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.IntegerField(default=1)
    content = models.TextField()
    pages = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    pages_completed = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    time_estimated = models.DurationField(default=timedelta(0), null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0), null=True, blank=True)
    slides = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    slides_completed = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order',]
        unique_together = ('course', 'parent_chapter', 'order')
        
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.pages is not None and self.pages_completed > self.pages:
            raise ValidationError({
                'pages_completed': 'Pages completed cannot be greater than total pages.'
            })

        if self.slides is not None and self.slides_completed > self.slides:
            raise ValidationError({
                'slides_completed': 'Slides completed cannot be greater than total slides.'
            })
    
    def save(self, *args, **kwargs):
        # auto increment order
        if not self.pk:
            max_order = Chapter.objects.filter(course=self.course, parent_chapter=self.parent_chapter).aggregate(models.Max('order'))['order__max']
            if max_order is not None:
                self.order = max_order + 1
                
        # Update the course's date_modified
        self.course.modified()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Decrement the order of chapters with a bigger order
        Chapter.objects.filter(course=self.course, parent_chapter=self.parent_chapter, order__gt=self.order).update(order=models.F('order') - 1)
        super().delete(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.course.pk})
    
    def complete(self):
        self.completed = True
        self.date_completed = timezone.now()
        self.pages_completed = self.pages
        self.slides_completed = self.slides
        self.progress = 100
        self.save()
        
    def uncomplete(self):
        self.completed = False
        self.date_completed = None
        self.pages_completed = self.get_pages_completed_during_studysessions()
        self.slides_completed = self.get_slides_completed_during_studysessions()
        self.calculate_progress()
        self.save()
        
    def get_remaining_pages(self):
        if self.pages is None:
            return None
        return self.pages - (self.pages_completed or 0)

    def get_remaining_slides(self):
        if self.slides is None:
            return None
        return self.slides - (self.slides_completed or 0)
    
    def studysession_changed(self, studysession):
        self.time_spent += studysession.time_spent
        self.pages_completed += studysession.pages_done
        self.slides_completed += studysession.slides_done
        self.calculate_progress()
        self.save()
    
    def get_pages_completed_during_studysessions(self):
        return self.studysession_set.aggregate(models.Sum('pages_done'))['pages_done__sum'] or 0
    
    def get_slides_completed_during_studysessions(self):
        return self.studysession_set.aggregate(models.Sum('slides_done'))['slides_done__sum'] or 0
    
    def calculate_progress(self):
        # Use getattr to get settings or None if they don't exist
        course_settings = getattr(self.course, 'settings', None)
        user_settings = getattr(self.course.user, 'settings', None)

        # Decide which settings to use
        settings = course_settings if course_settings else user_settings
        if not settings:
            raise ValidationError('No settings found for this chapter')

        # Progress calculation
        page_progress = (self.pages_completed / self.pages) if self.pages else 0
        slide_progress = (self.slides_completed / self.slides) if self.slides else 0
        time_progress = min((self.time_spent / self.time_estimated if self.time_estimated else 0), 1)  # Time progress cannot be greater than 1

        total_progress = (settings.page_weight * page_progress + settings.slide_weight * slide_progress + settings.time_weight * time_progress) * 100
        self.progress = total_progress
