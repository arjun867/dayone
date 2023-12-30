from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username

class Task(models.Model):
    title = models.CharField(max_length=150)
    created_time = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # Add the completed field here
    users = models.ManyToManyField(User, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.title

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    date = models.DateField()
    day = models.CharField(max_length=10)
    content = models.TextField()

    def __str__(self):
        return f"Journal Entry ({self.date})"

    def save(self, *args, **kwargs):
        self.day = self.date.strftime("%A")
        super().save(*args, **kwargs)
