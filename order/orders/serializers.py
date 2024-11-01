from rest_framework import serializers
from .models import UserProfile, Category
from .models import Restaurant, Menu, OptionGroup, OptionItem


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
    options = OptionGroupSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'image_url', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        menu = Menu.objects.create(**validated_data)  # 메뉴 객체 생성

        # 각 옵션 그룹 및 옵션 항목 저장
        for option_group_data in options_data:
            option_group = OptionGroup.objects.create(name=option_group_data['name'])  # 새 옵션 그룹 생성
            for option_data in option_group_data['options']:
                OptionItem.objects.create(group=option_group, **option_data)  # 옵션 항목 생성

        return menu  # 생성된 메뉴 객체 반환