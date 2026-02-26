import pytest
from django.urls import reverse
from .models import Category

@pytest.mark.django_db
def test_home_page_status():
    url = reverse('home')
    assert url == '/'

@pytest.mark.django_db
def test_login_page_status(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_page_status(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Study")
    assert category.name == "Study"

@pytest.mark.django_db
def test_category_string_representation():
    category = Category.objects.create(name="Work")
    assert str(category) == "Work"