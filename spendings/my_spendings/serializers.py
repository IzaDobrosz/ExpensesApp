from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Expense

# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, allow_blank=False, max_length=100)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Category` instance, given the validated data.
#         """
#         return Category.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Category` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.save()
#         return instance
#
#
# class ExpenseSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, allow_blank=False, max_length=160)
#     amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
#     date = serializers.DateField(required=True, format='%d-%m-%Y')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Expense` instance, given the validated data.
#         """
#         return Expense.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Expense` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.amount = validated_data.get('amount', instance.amount)
#         instance.date = validated_data.get('date', instance.date)
#         instance.save()
#         return instance


# ModelSerializer
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name']


# class UserSerializer(serializers.ModelSerializer):
#     categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'categories', 'owner']


# Hyperlink
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
   Serializer for the Category model.

   This serializer converts Category model instances into representations
   that can be rendered into JSON or other content types. It includes the
   category's URL, ID, name, and the owner's username (read-only).
   """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'owner']


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Expense model.

    This serializer converts Expense model instances into representations
    that can be rendered into JSON or other content types. It includes the
    expense's URL, ID, name, amount, date, owner's username (read-only), and
    category it belongs to.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Expense
        fields = ['url', 'id', 'name', 'amount', 'date', 'owner', 'category']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
   Serializer for the User model.

   This serializer converts User model instances into representations
   that can be rendered into JSON or other content types. It includes the
   user's URL, ID, username, and their related categories (read-only).
   """
    categories = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'categories']
