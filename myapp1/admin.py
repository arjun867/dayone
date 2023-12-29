from django.contrib import admin

# Register your models here.
from .models import User,Task,JournalEntry

admin.site.register(User)
admin.site.register(Task)
admin.site.register(JournalEntry)