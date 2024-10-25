from rest_framework import serializers
from .models import UserProfile, Category
from .models import Restaurant


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # user 필드를 기본 키로 설정

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'address']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone_number', 'rating', 'owner', 'categories', 'operating_hours', 'description', 'image_url', 'delivery_fee']