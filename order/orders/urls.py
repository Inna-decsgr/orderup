from django.urls import path
from .views import login_view, signup_view, update_user

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # 회원가입 URL
    path('login/', login_view, name='login'),  # 로그인 URL
    path('edituser/<int:user_id>/', update_user, name='edituser'), # 사용자 정보 수정 URL
]