from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Category

# 1. Home Page (Public)
def home(request):
    return render(request, 'core/home.html')

# 2. Registration Page (Public)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 3. Task List (Private - Login Required)
@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'core/task_list.html', {'tasks': tasks})

# 4. Create Task (Private - CRUD)
@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        Task.objects.create(title=title, category=category, owner=request.user)
        return redirect('task_list')
    categories = Category.objects.all()
    return render(request, 'core/task_form.html', {'categories': categories})

# 5. Delete Task (Private - CRUD)
@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk, owner=request.user)
    task.delete()
    return redirect('task_list')