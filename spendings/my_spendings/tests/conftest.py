import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from my_spendings.models import Category, Expense


@pytest.fixture
def api_client():
    """
    Fixture to create and return an instance of APIClient.

    This fixture provides a pre-configured APIClient that can be used
    to simulate HTTP requests to the Django REST framework API. It allows
    tests to perform actions like GET, POST, PUT, DELETE on API endpoints
    and inspect responses, headers, and status codes.
    """
    return APIClient()


@pytest.fixture
def user(db):
    """
    Fixture to create a sample user.
    """
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def category(user):
    """
    Fixture to create a sample category owned by the user.
    """
    return Category.objects.create(name="Test Category", owner=user)


@pytest.fixture
def expense(category, user):
    """
    Fixture to create an expense for testing purposes.
    """
    return Expense.objects.create(
        name='Test Expense',
        amount=100,
        category=category,
        date='2024-01-01',
        owner=user)
