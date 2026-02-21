from django.db import models
from django.contrib.auth.models import User

# Model 1: Category (Many-to-One relationship with Task)
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

# Model 2: Tag (Many-to-Many relationship with Task)
class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

# Model 3: Task (The core model)
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Many-to-One [cite: 22]
    tags = models.ManyToManyField(Tag) # Many-to-Many [cite: 23]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)