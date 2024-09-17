import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from my_spendings.models import Category, Expense
from my_spendings.tests.conftest import category


@pytest.mark.django_db
def test_create_user(api_client):   # Use the fixture 'api_client
    url = reverse('user-list')      # Use 'reverse' to generate the URL for the 'user-list' view
    response = api_client.post(url, {'username': 'testuser', 'password': 'testpass'})

    assert response.status_code == 405  # Check if the response status is 401 Method not allowed


@pytest.mark.django_db
def test_category_list_unauthenticated_access():
    # Create an instance of APIClient for testing
    client = APIClient()

    # Endpoint URL for CategoryList
    url = reverse('category-list')

    # Test GET request (listing categories) - should be allowed
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK  # Unauthenticated users can still list categories

    # Test POST request (creating a category) - should be forbidden for unauthenticated users
    data = {'name': 'Test Category'}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Unauthenticated users cannot create categories


@pytest.mark.django_db
def test_category_detail_unauthenticated(api_client, category):
    """
    Test that an unauthenticated user can retrieve a category
    but cannot update or delete it.
    """
    url = reverse('category-detail', args=[category.id])  # Generate the URL for category detail view

    # Attempt to retrieve the category (should be allowed)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK  # Unauthenticated users can retrieve

    # Attempt to update the category (should be denied)
    response = api_client.put(url, {'name': 'Updated Category'})
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Unauthenticated users cannot update

    # Attempt to delete the category (should be denied)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Unauthenticated users cannot delete


@pytest.mark.django_db
def test_expense_list_unauthenticated(api_client, expense):
    """
    Test that an unauthenticated user can retrieve a list of expenses
    but cannot create a new expense.
    """
    url = reverse('expense-list')  # Generate the URL for expense list view

    # Attempt to retrieve the expense list (should be allowed for unauthenticated users)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK  # Unauthenticated users can view the list

    # Attempt to create a new expense (should be denied for unauthenticated users)
    data = {
        'name': 'New Test Expense',
        'amount': 200,
        'date': '2024-01-02',
        'category': expense.category.id  # Use the category ID from the fixture
    }
    response = api_client.post(url, data)

    # Expecting 403 Forbidden for unauthenticated users trying to create a new expense
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Unauthenticated users cannot create new expenses


@pytest.mark.django_db
def test_expense_detail_unauthenticated(api_client, expense):
    """
    Test that an unauthenticated user can retrieve expense details
    but cannot update or delete the expense.
    """
    # Generate the URL for the specific expense detail view
    url = reverse('expense-detail', args=[expense.id])

    # Attempt to retrieve the expense detail (should be allowed)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK  # Unauthenticated users can retrieve the expense

    # Attempt to update the expense (should be denied)
    update_data = {
        'name': 'Updated Expense',
        'amount': 500
    }
    response = api_client.put(url, update_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Unauthenticated users cannot update

    # Attempt to delete the expense (should be denied)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN  # Unauthenticated users cannot delete


@pytest.mark.django_db
def test_create_category_logged_in(api_client, user):
    # Zamiast sprawdzania len(response.data), sprawdzamy len(response.data['results']),
    # ponieważ response.data zawiera paginowaną strukturę,
    # gdzie lista wyników znajduje się w kluczu results.
    """
    Test that a logged-in user can create a category and see it in the list.
    This test verifies that:
    1. The category list is initially empty.
    2. A new category can be created.
    3. The created category appears in the list.
    """
    # Authenticate the user in the API client
    api_client.force_authenticate(user=user)

    # Initially, the category list should be empty
    url = reverse('category-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 0  # Check the paginated 'results' list

    # Create a new category
    post_data = {'name': 'New Category'}
    response = api_client.post(url, post_data)
    assert response.status_code == status.HTTP_201_CREATED  # Check if creation was successful

    # Verify the category appears in the list
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1  # Now there should be one category in 'results'
    assert response.data['results'][0]['name'] == 'New Category'  # The created category should be in the response

    # Check if the category exists in the database
    assert Category.objects.count() == 1
    assert Category.objects.first().name == 'New Category'
    assert Category.objects.all().count() == 1


@pytest.mark.django_db
def test_get_category_detail_logged_in(api_client, user, category):
    """
    Test that a logged-in user can retrieve the details of a single category.
    """
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Send GET request to retrieve the category by its ID
    url = reverse('category-detail', args=[category.id])
    response = api_client.get(url)

    # Check if the request was successful and the category is returned
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == category.name  # Ensure the correct category is returned
    assert response.data['id'] == category.id  # Ensure the correct category ID is returned
    assert response.data['owner'] == user.username  # Ensure the category belongs to the logged-in user


@pytest.mark.django_db
def test_put_category_update_logged_in(api_client, user, category):
    """
    Test that a logged-in user can update a category's name using PUT.
    """
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Send PUT request to update the category's name
    url = reverse('category-detail', args=[category.id])
    updated_data = {'name': 'Updated Category'}
    response = api_client.put(url, updated_data)

    # Check if the request was successful
    assert response.status_code == status.HTTP_200_OK

    # Ensure the category's name is updated in the database
    category.refresh_from_db()  # Reload the category from the database
    assert category.name == 'Updated Category'


@pytest.mark.django_db
def test_patch_category_update_logged_in(api_client, user, category):
    """
    Test that a logged-in user can partially update a category's name using PATCH.
    """
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Send PATCH request to partially update the category's name
    url = reverse('category-detail', args=[category.id])
    patch_data = {'name': 'Partially Updated Category'}
    response = api_client.patch(url, patch_data)

    # Check if the request was successful
    assert response.status_code == status.HTTP_200_OK

    # Ensure the category's name is updated in the database
    category.refresh_from_db()  # Reload the category from the database
    assert category.name == 'Partially Updated Category'


@pytest.mark.django_db
def test_create_expense_logged_in(api_client, user, category):
    # Zamiast sprawdzania len(response.data), sprawdzamy len(response.data['results']),
    # ponieważ response.data zawiera paginowaną strukturę,
    # gdzie lista wyników znajduje się w kluczu results.
    """
    Test that a logged-in user can create an expense and see it in the list.
    """
    # Authenticate the user in the API client
    api_client.force_authenticate(user=user)

    # Initially, the expense list should be empty
    url = reverse('expense-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 0  # Check the paginated 'results' list

    # Create a new expense (use the full URL for the category)
    category_url = reverse('category-detail', args=[category.id])
    post_data = {
        'name': 'New Expense',
        'amount': 200,
        'category': category_url,  # Pass the full URL for the category, because of hiperlink
        'date': '2024-01-01'
    }
    response = api_client.post(url, post_data)

    # Log the response in case of error to diagnose the issue
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        print("Response data:", response.data)

    # Assert the creation was successful
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the expense appears in the list
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1  # Now there should be one expense in 'results'
    assert response.data['results'][0]['name'] == 'New Expense'  # The created expense should be in the response

    # Check if the expense exists in the database
    assert Expense.objects.count() == 1
    assert Expense.objects.first().name == 'New Expense'


@pytest.mark.django_db
def test_get_expense_detail_logged_in(api_client, user, expense):
    """
    Test that a logged-in user can retrieve the details of a single expense.
    """
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Send GET request to retrieve the expense by its ID
    url = reverse('expense-detail', args=[expense.id])
    response = api_client.get(url)

    # Check if the request was successful and the expense is returned
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == expense.name  # Ensure the correct expense is returned
    assert response.data['id'] == expense.id  # Ensure the correct expense ID is returned
    assert response.data['amount'] == expense.amount  # Ensure the correct expense amount is returned

    # Compare the category URL
    category_url = reverse('category-detail', args=[expense.category.id])
    assert response.data[
               'category'] == f'http://testserver{category_url}'  # Ensure the correct expense category is returned

    # Ensure the expense belongs to the logged-in user
    assert response.data['owner'] == user.username


@pytest.mark.django_db
def test_put_expense_update_logged_in(api_client, user, expense, category):
    """
    Test that a logged-in user can update a expense's name using PUT.
    """
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Send PUT request to update the expense's name
    url = reverse('expense-detail', args=[expense.id])
    # Ensure to include all necessary fields from model for PUT
    updated_data = {
        'name': 'Updated Expense',
        'amount': 500,
        'category': reverse('category-detail', args=[category.id]),
        'date': '2024-01-01'
    }
    response = api_client.put(url, updated_data)

    # Check if the request was successful
    assert response.status_code == status.HTTP_200_OK

    # Ensure the expense's name is updated in the database
    expense.refresh_from_db()  # Reload the expense from the database
    assert expense.name == 'Updated Expense'
    assert expense.amount == 500


@pytest.mark.django_db
def test_patch_expense_update_logged_in(api_client, user, category, expense):
    """
    Test that a logged-in user can partially update a expense's name using PATCH.
    """
    # Authenticate the user
    api_client.force_authenticate(user=user)

    # Send PATCH request to partially update the expense's name
    url = reverse('expense-detail', args=[expense.id])
    patch_data = {'name': 'Partially Updated expense'}
    response = api_client.patch(url, patch_data)

    # Check if the request was successful
    assert response.status_code == status.HTTP_200_OK

    # Ensure the expense's name is updated in the database
    expense.refresh_from_db()  # Reload the expense from the database
    assert expense.name == 'Partially Updated expense'
