from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import UserProfile
from rest_framework import status
from orders.models import UserProfile  


# 회원가입
@api_view(['POST'])
def signup_view(request):
    username = request.data.get('name')
    email = request.data.get('signupid')
    password = request.data.get('signuppassword')
    phone_number = request.data.get('phoneNumber')
    address = request.data.get('address')

    # 필수 데이터 누락 확인
    if not username or not email or not password:
        return Response({"error": "이름, 아이디, 비밀번호는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 이메일 중복 체크
    if User.objects.filter(email=email).exists():  # User 모델에서 이메일 확인
        return Response({"error": "이미 사용 중인 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 사용자 생성
    user = User.objects.create_user(username=username, email=email, password=password)

    # UserProfile 정보 저장
    UserProfile.objects.create(user=user, phone_number=phone_number, address=address)

    return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)


# 로그인
@api_view(['POST'])
def login_view(request):
    email = request.data.get('loginid')  # loginid를 이메일로 받음
    password = request.data.get('loginpassword')
    
    user = authenticate(request, username=email, password=password)  # username 대신 email로 처리
    if user is not None:
        login(request, user)
        
        # UserProfile 에서 사용자 정보 가져오기
        try:
            profile = UserProfile.objects.get(user=user)
            phone_number = profile.phone_number
            address = profile.address
        except UserProfile.DoesNotExist:
            phone_number = None  # UserProfile이 없을 경우 None 처리
            address = None
            
        return JsonResponse({
            'message': '로그인 성공',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'phone_number' : phone_number,
                'address': address,
            }
        })
    else:
        return JsonResponse({'message': '아이디 또는 비밀번호가 잘못되었습니다.'}, status=400)


