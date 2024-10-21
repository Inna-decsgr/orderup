from django.urls import path
from .views import login_view, signup_view, update_user, get_user, delete_user

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # 회원가입 URL
    path('login/', login_view, name='login'),  # 로그인 URL
    path('edituser/<int:user_id>/', update_user, name='edituser'), # 사용자 정보 수정 URL
    path('getuser/<int:user_id>/', get_user, name='getuser'), # 사용자 정보 조회 URL
    path('deleteuser/<int:user_id>/', delete_user, name='deleteuser'), # 사용자 정보 삭제 URL
]