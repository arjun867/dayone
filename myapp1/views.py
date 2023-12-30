from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError

from .models import Task, JournalEntry,User

@login_required
def home(request):
    user = request.user
    todos = Task.objects.filter(users=user, completed=False)
    completed_tasks = user.tasks.filter(completed=True).order_by('-created_time')[:15]
    today = timezone.localdate()
    content = ""
    try:
        today_entry = JournalEntry.objects.get(user=user, date=today)
        content = today_entry.content
    except JournalEntry.DoesNotExist:
        pass

    return render(request, 'layout.html', {'todos': todos, 'completed_tasks': completed_tasks, 'content': content})

@login_required
def add_task(request):
    if request.method == 'POST':
        new_task_title = request.POST.get('task', '')
        if new_task_title:
            task = Task.objects.create(title=new_task_title)
            task.users.add(request.user)
        return redirect('home')
    return render(request, 'layout.html')

@login_required
def mark_completed(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = True
    task.save()
    return redirect('home')

@login_required
def remark(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = False
    task.save()
    return redirect('home')

@login_required
def create_entry(request):
    today = timezone.localdate()
    if request.method == "POST":
        content = request.POST["content"]
        entry, created = JournalEntry.objects.get_or_create(date=today, user=request.user)
        entry.content = content
        entry.save()
        return redirect("view_all")
    else:
        return redirect("home")

@login_required
def view_all(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by("-date")
    return render(request, "view_all.html", {"entries": entries})
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "register.html")


def about(request):
    return render(request,"about.html")

def help(request):
    return render(request,"help.html")

