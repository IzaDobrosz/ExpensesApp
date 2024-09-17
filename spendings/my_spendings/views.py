# # variant 1
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# # variant 2
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# # variant 3
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# # variant 4
# from rest_framework import mixins
# from rest_framework import generics

# variant 5
from rest_framework import generics

# user
from django.contrib.auth.models import User
from my_spendings.serializers import UserSerializer
from rest_framework import permissions
from my_spendings.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from my_spendings.models import Category, Expense
from my_spendings.serializers import CategorySerializer, ExpenseSerializer

# variant 1 Basic/primitive
# @csrf_exempt
# def category_list(request):
#     """
#     List all categories, or create a new category.
#     """
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = CategorySerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def category_detail(request, pk):
#     """
#     Retrieve, update or delete a category.
#     """
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = CategorySerializer(category, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         category.delete()
#         return HttpResponse(status=204)


# variant 2 Wrapping API views
# @api_view(['GET', 'POST'])
# def category_list(request, format=None):
#     """
#     List all categories, or create a new category.
#     """
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a category.
#     """
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
##
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # variant 3 Class-based Views
# class CategoryList(APIView):
#     """
#     List all categories, or create a new category.
#     """
#     def get(self, request, format=None):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CategoryDetail(APIView):
#     name = 'category_detail'
#     """
#     Retrieve, update or delete a category.
#     """
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     def delete(self, request, pk, format=None):
#         category = self.get_object(pk)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# variant 4 Mixins
# class CategoryList(mixins.ListModelMixin,
#                    mixins.CreateModelMixin,
#                    generics.GenericAPIView):
#     """
#     List all categories, or create a new category.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class CategoryDetail(mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin,
#                      generics.GenericAPIView):
#     """
#     Retrieve, update or delete a category.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# variant 5 generic class-based views
class CategoryList(generics.ListCreateAPIView):
    """
    List all categories, or create a new category.

    This view handles two operations:
    1. GET: Returns a list of all categories. This is available to both authenticated
       and unauthenticated users, as per the IsAuthenticatedOrReadOnly permission.
    2. POST: Allows an authenticated user to create a new category. The 'owner' of the
       category is automatically set to the currently logged-in user.

    The 'perform_create' method ensures that the 'owner' field is populated with the
    user making the request when a new category is created.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category.

    This view allows users to:
    1. GET: Retrieve the details of a specific category by its ID. Available to all users.
    2. PUT/PATCH: Update the details of a specific category. Only the owner of the category
       can perform this action.
    3. DELETE: Remove a category from the database. Only the owner can delete it.

    The IsOwnerOrReadOnly permission ensures that only the category's owner can modify
    or delete the category, while other users can only view it.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class ExpenseList(generics.ListCreateAPIView):
    """
   List all expenses or create a new expense.

   This view allows users to:
   1. GET: Retrieve a list of all expenses. Available to all users.
   2. POST: Create a new expense. The expense is associated with the currently logged-in user.

   The IsAuthenticatedOrReadOnly permission ensures that creating a new expense requires authentication,
   but viewing the list of expenses is accessible to all users.
   """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Save a new expense with the owner set to the currently authenticated user.
        """
        serializer.save(owner=self.request.user)


class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an expense.

    This view allows users to:
    1. GET: Retrieve the details of a specific expense by its ID. Available to all users.
    2. PUT/PATCH: Update the details of a specific expense. Only the owner of the expense
       can perform this action.
    3. DELETE: Remove an expense from the database. Only the owner can delete it.

    The IsOwnerOrReadOnly permission ensures that only the expense's owner can modify or delete
    the expense, while other users can only view it.
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    """
    API view to retrieve a list of users.

    This view provides a `GET` method handler to list all users in the system.
    It uses Django REST framework's `ListAPIView` to provide a read-only endpoint
    for the User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    API view to retrieve a single user instance by ID.

    This view provides a `GET` method handler to fetch details of a single user.
    It uses Django REST framework's `RetrieveAPIView` to provide a read-only endpoint
    for retrieving user details.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    Root view for the API.

    This view provides a central entry point for the API, returning a list of
    available endpoints. It supports the GET method and returns hyperlinks to
    the 'user-list', 'category-list', and 'expense-list' endpoints in order to help
    users to navigate to different parts of the API.

    Args:
        request: The HTTP request object.
        format: Optional format suffix for the URLs.

    Returns:
        Response: A dictionary containing the API's main endpoints.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'expenses': reverse('expense-list', request=request, format=format)
    })
