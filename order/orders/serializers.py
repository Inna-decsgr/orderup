from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # user 필드를 기본 키로 설정

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'address']
