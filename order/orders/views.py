from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import UserProfile
from rest_framework import status
from orders.models import UserProfile  
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from .serializers import RestaurantSerializer
from rest_framework import generics
from .models import Restaurant, Category
from decimal import Decimal, InvalidOperation



# 회원가입
@api_view(['POST'])
def signup_view(request):
    username = request.data.get('name')
    email = request.data.get('signupid')
    password = request.data.get('signuppassword')
    phone_number = request.data.get('phoneNumber')
    address = request.data.get('address')
    is_owner = request.data.get('isOwner')
    reg_number = request.data.get('regnumber')

    # 필수 데이터 누락 확인
    if not username or not email or not password:
        return Response({"error": "이름, 아이디, 비밀번호는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 이메일 중복 체크
    if User.objects.filter(email=email).exists():  # User 모델에서 이메일 확인
        return Response({"error": "이미 사용 중인 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 새로운 사용자 생성
    user = User.objects.create_user(username=username, email=email, password=password)

    # UserProfile 정보 저장
    UserProfile.objects.create(user=user, phone_number=phone_number, address=address, is_owner=is_owner, business_registration_number=reg_number)

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
            regnumber = profile.business_registration_number
            isowner = profile.is_owner
        except UserProfile.DoesNotExist:
            phone_number = None  
            address = None
            
        return JsonResponse({
            'message': '로그인 성공',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'phone_number' : phone_number,
                'address': address,
                'business_registration_number': regnumber,
                'is_owner': isowner
            }
        })
    else:
        return JsonResponse({'message': '아이디 또는 비밀번호가 잘못되었습니다.'}, status=400)




# 사용자 정보 수정
@api_view(['PUT'])
def update_user(request, user_id):
    try:
        # UserProfile 객체 가져오기
        user_profile = UserProfile.objects.get(user__id=user_id)
        # User 객체 가져오기
        user = user_profile.user

        # 요청 데이터에서 사용자 정보 가져오기
        username = request.data.get('username', user.username)  # 이름 업데이트
        email = request.data.get('email', user.email)  # 이메일 업데이트
        phone_number = request.data.get('phone_number', user_profile.phone_number)  # 전화번호 업데이트
        address = request.data.get('address', user_profile.address)  # 주소 업데이트
        is_owner = request.data.get('is_owner', user_profile.is_owner)  # 사업자 여부 업데이트
        business_registration_number = request.data.get('business_registration_number', user_profile.business_registration_number)  # 사업자 등록 번호 업데이트

        # User 객체 업데이트
        user.username = username
        user.email = email
        user.save()  # User 객체 저장

        # UserProfile 객체 업데이트
        user_profile.phone_number = phone_number
        user_profile.address = address
        user_profile.is_owner = is_owner  # 사업자 여부 업데이트
        user_profile.business_registration_number = business_registration_number  # 사업자 등록 번호 업데이트
        user_profile.save()  # UserProfile 객체 저장

        return Response({
            'message': '사용자 정보가 업데이트되었습니다.',
            'user': {
                'username': user.username,
                'email': user.email,
                'phone_number': user_profile.phone_number,
                'address': user_profile.address,
                'is_owner': user_profile.is_owner,
                'business_registration_number': user_profile.business_registration_number
            }
        }, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 사용자 정보 조회하는 뷰
@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        userprofile = UserProfile.objects.get(user=user)
        data = {
            'id': user_id,
            'username': user.username,
            'email': user.email,
            'phone_number': userprofile.phone_number,
            'address': userprofile.address,
            'is_owner': userprofile.is_owner,
            'business_registration_number': userprofile.business_registration_number,
        }
        return JsonResponse(data) 
    except User.DoesNotExist:
        return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
    



# 사용자 정보 삭제하는 뷰
def delete_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        user.delete()  # 사용자 삭제
        return JsonResponse({'message': '사용자가 성공적으로 삭제되었습니다.'}, status=204)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    


# csrftoken 가져오는 뷰
@api_view(['GET'])
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})



# 인증된 사용자만 새로운 Restaurant 인스턴스 생성할 수 있는 APIView 정의 
class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def perform_create(self, serializer):
        # 요청 데이터에서 카테고리 ID를 가져옴
        category_ids = self.request.data.get('categories', [])
        print(category_ids)
        
        # 평점과 배달 요금을 Decimal로 변환
        try:
            rating = Decimal(self.request.data.get('rating'))  # 평점을 Decimal로 변환
            delivery_fee = Decimal(self.request.data.get('delivery_fee'))  # 배달 요금을 Decimal로 변환
        except (ValueError, InvalidOperation):
            # 잘못된 데이터 형식일 경우 오류 반환
            return Response({"error": "Invalid data format for rating or delivery fee."}, status=status.HTTP_400_BAD_REQUEST)

        # 레스토랑 객체를 저장하고, 저장된 객체의 ID를 통해 관계 추가
        restaurant = serializer.save(rating=rating, delivery_fee=delivery_fee)

        # 카테고리 ID 리스트로부터 Category 객체를 찾아서 ManyToMany 필드에 추가
        categories = Category.objects.filter(id__in=category_ids)
        restaurant.categories.set(categories)


# 가게 등록하는 뷰
@api_view(['POST'])
def store_regis(request):
    print(request.data)
    if request.method == 'POST':
        # 클라이언트에서 보낸 데이터 추출
        name = request.data.get('name')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number', None)
        rating = request.data.get('rating')
        owner = request.data.get('owner')  # owner는 User의 ID 또는 객체일 것으로 예상됨
        categories = request.data.get('categories', [])
        operating_hours = request.data.get('operating_hours', None)
        description = request.data.get('description')
        image_url = request.data.get('image_url', None)
        delivery_fee = request.data.get('deliveryfee', 500.0)

        print("Received image_url:", phone_number)
        # 새로운 Restaurant 객체 생성
        restaurant_data = {
            'name': name,
            'address': address,
            'phone_number': phone_number,
            'rating': rating,
            'owner': owner,
            'operating_hours': operating_hours,
            'description': description,
            'image_url': image_url,
            'delivery_fee': delivery_fee,
            'categories': categories 
        }

        serializer = RestaurantSerializer(data=restaurant_data)

        if serializer.is_valid():
            restaurant = serializer.save()  # Restaurant 객체 저장
            restaurant.categories.set(categories)  # ManyToMany 관계 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)