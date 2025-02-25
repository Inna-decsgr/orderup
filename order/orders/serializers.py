from rest_framework import serializers
from .models import UserProfile, Category
from .models import Restaurant, Menu, OptionGroup, OptionItem, Rider
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
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'rating', 'owner', 'categories',
        'operating_hours', 'description', 'image_url', 'delivery_fee']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:  
            return request.build_absolute_uri(obj.image.url)  # `image.url` 자동 반환
        return obj.image_url  # 기존 URL이 있다면 그대로 반환


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

    def validate(self, attrs):
        options_data = self.initial_data.get('options')
        
        if options_data:
            # options가 이미 리스트 형식인지 확인
            if isinstance(options_data, str):
                try:
                    attrs['options'] = json.loads(options_data)
                except json.JSONDecodeError as e:
                    raise serializers.ValidationError("Invalid JSON format for options")
            elif isinstance(options_data, list):
                attrs['options'] = options_data
            else:
                raise serializers.ValidationError("options must be a JSON string or list format")
        
        return attrs

    def create(self, validated_data):
        print("validated_data:", validated_data)
        restaurant_id = validated_data.pop('restaurant_id', None)  # 전달된 restaurant_id 가져오기
        options_data = validated_data.pop('options', []) # 전달된 options 배열 가져오기
        print("options_data:", options_data)

        # restaurant_id가 있는 경우 해당 ID에 해당하는 Restaurant 객체 찾기
        restaurant = get_object_or_404(Restaurant, id=restaurant_id) if restaurant_id else None

        # Menu 객체 생성 시 restaurant 필드에서 찾은 Restaurant 객체 할당
        menu = Menu.objects.create(restaurant=restaurant, **validated_data)  # 메뉴 객체 생성



        # 각 옵션 그룹 및 옵션 항목 저장
        for option_group_data in options_data:
            option_group = OptionGroup.objects.create(name=option_group_data['name'], menu=menu)   # 새 옵션 그룹 생성
            
            for option_data in option_group_data.get('options', []):
                OptionItem.objects.create(group=option_group, name=option_data.get('name'), price=option_data.get('price'))

        
        return menu  # 생성된 메뉴 객체 반환
    


class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ['id', 'name', 'phone_number']
