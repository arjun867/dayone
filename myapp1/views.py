from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils import timezone


from .models import User,Task,JournalEntry
# Create your views here.
def home(request):
    if 'tasks' not in request.session:
        request.session['tasks'] = []

    completed_tasks = Task.objects.filter(is_completed=True).order_by('-created_time')
    todos = Task.objects.filter(is_completed=False)

    if len(completed_tasks)>15:
        # Get the 15 oldest completed tasks
        tasks_to_remove = completed_tasks[:len(completed_tasks) - 15]

        # Delete the tasks from the database
        for task in tasks_to_remove:
            task.delete()
     
    today = timezone.localdate()
    content = request.session.get("journal_content", "")  # Retrieve from session or use empty string

    if not content:  # Check if content is still empty
        try:
            todays_entry = JournalEntry.objects.get(date=today)
            content = todays_entry.content
            request.session["journal_content"] = content  # Store in session for subsequent views
        except JournalEntry.DoesNotExist:
            pass

    context = {
        'todos': todos,
        'completed_tasks': completed_tasks,
        'content':content
    }
    return render(request, 'layout.html', context)


def add_task(request):
    
    if request.method == 'POST':
        new_task = request.POST['task']
        request.session['tasks'].append(new_task)

        # Create a new Task object for persistence
        Task.objects.create(title=new_task)

        return redirect('home')

def mark_completed(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = True
    task.save()

    return redirect('home')

def remark(request,task_id):
    task=Task.objects.get(id=task_id)
    task.is_completed=False
    task.save()

    return redirect('home')

# def delete(request,task_id):
#     Task.objects.remove(id=task_id)
#     # task.save()
#     return redirect('home')

def create_entry(request):
    today = timezone.localdate()

    if request.method == "POST":
        content = request.POST["content"]

        # Check for existing entry and update or create
        entry, created = JournalEntry.objects.get_or_create(date=today, defaults={"content": content})
        entry.content = content  # Overwrite content in either case
        entry.save()

        request.session["journal_content"] = content  # Store in session for other views

        return redirect("view_all")
    else:
        # Content will be handled in the home view
        return redirect("home")

def view_all(request):
    entries = JournalEntry.objects.order_by("-date")
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

