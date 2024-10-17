from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # 이메일로 사용자 찾기
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        # 비밀번호가 맞으면 로그인
        if user.check_password(password):
            return user
        return None
