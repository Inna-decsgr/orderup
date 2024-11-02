from rest_framework import serializers
from .models import UserProfile, Category
from .models import Restaurant, Menu, OptionGroup, OptionItem
from django.shortcuts import get_object_or_404
import json


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


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionItem
        fields = ['name', 'price']

class OptionGroupSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # 옵션 목록을 포함

    class Meta:
        model = OptionGroup
        fields = ['name', 'options']


class MenuSerializer(serializers.ModelSerializer):
    options = OptionGroupSerializer(many=True, required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'image', 'image_url', 'options']

    def create(self, validated_data):
        restaurant_id = validated_data.pop('restaurant_id', None)  # 전달된 restaurant_id 가져오기
        options_data = validated_data.pop('options', []) # 전달된 options 배열 가져오기

        # restaurant_id가 있는 경우 해당 ID에 해당하는 Restaurant 객체 찾기
        restaurant = get_object_or_404(Restaurant, id=restaurant_id) if restaurant_id else None

        # Menu 객체 생성 시 restaurant 필드에서 찾은 Restaurant 객체 할당
        menu = Menu.objects.create(restaurant=restaurant, **validated_data)  # 메뉴 객체 생성

        # 각 옵션 그룹 및 옵션 항목 저장
        for option_group_data in options_data:
            option_group = OptionGroup.objects.create(name=option_group_data['name'], menu=menu)   # 새 옵션 그룹 생성
            for option_data in option_group_data['options']:
                option_name = option_data.get('name')
                option_price = option_data.get('price')
                OptionItem.objects.create(group=option_group, name=option_name, price=option_price)  # 옵션 항목 생성

        return menu  # 생성된 메뉴 객체 반환