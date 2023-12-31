from django.db import models
from django.contrib.auth.models import User
from PIL import Image # Resize image using Pillow

from planner.models.settings import UserSettings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Must be checked before saving
        super().save(*args, **kwargs)

        if is_new:
            UserSettings.objects.create(user=self.user)
        
        img = Image.open(self.image)
        # Resize image to 300x300 if it is larger than that
        if img.height > 300 or img.width > 300:
            output_size = (300, 300) 
            img.thumbnail(output_size)
            img.save(self.image.path)
        


