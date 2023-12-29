from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    pass

class Task(models.Model):
    title=models.CharField(max_length=150)
    is_completed=models.BooleanField(default=False)
    created_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.title
    
class JournalEntry(models.Model):
    date = models.DateField(default=timezone.now)
    day = models.CharField(max_length=10)  # Weekday name
    content = models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return f"Journal Entry ({self.date})"

    def save(self, *args, **kwargs):
        self.day = self.date.strftime("%A")  # Automatically set weekday
        super().save(*args, **kwargs)