from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Category, Tag

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
    # prefetch_related optimizes database queries for Many-to-Many fields
    tasks = Task.objects.filter(owner=request.user).prefetch_related('tags')
    return render(request, 'core/task_list.html', {'tasks': tasks})

# 4. Create Task (Private - CRUD)
@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        
        # 1. Create the task first
        task = Task.objects.create(title=title, description=description, category=category, owner=request.user)
        
        # 2. Save the Many-to-Many Tags
        tag_ids = request.POST.getlist('tags')
        task.tags.set(tag_ids)
        
        return redirect('task_list')
        
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'core/task_form.html', {'categories': categories, 'tags': tags})

# 5. Delete Task (Private - CRUD)
@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk, owner=request.user)
    task.delete()
    return redirect('task_list')

# 6. Update Task (Private - CRUD)
@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk, owner=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        task.category = Category.objects.get(id=category_id)
        task.save()

        # Update Many-to-Many Tags
        tag_ids = request.POST.getlist('tags')
        task.tags.set(tag_ids)
        
        return redirect('task_list')
        
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'core/task_update.html', {'task': task, 'categories': categories, 'tags': tags})