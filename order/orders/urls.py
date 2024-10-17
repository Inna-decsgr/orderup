from django.urls import path
from .views import login_view, signup_view 

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # 회원가입 URL
    path('login/', login_view, name='login'),  # 로그인 URL
]