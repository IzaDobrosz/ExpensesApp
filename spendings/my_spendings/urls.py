from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from my_spendings import views

urlpatterns = format_suffix_patterns([
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', views.api_root),
    path('expenses', views.ExpenseList.as_view(), name='expense-list'),
    path('expence/<int:pk>/', views.ExpenseDetail.as_view(), name='expense-detail'),
])

# urlpatterns = format_suffix_patterns(urlpatterns)
