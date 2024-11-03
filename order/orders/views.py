from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import UserProfile, Restaurant
from rest_framework import status
from orders.models import UserProfile, Menu, OptionGroup, OptionItem
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from .serializers import RestaurantSerializer
from rest_framework import generics
from decimal import Decimal, InvalidOperation
from django.core.files.storage import FileSystemStorage
from .serializers import MenuSerializer 
import json




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
        



# 가게 정보 조회하는 뷰
@api_view(['GET'])
def my_store_view(request, user_id):
    try:
        # owner_id가 user_id와 일치하는 레코드 조회
        restaurants = Restaurant.objects.filter(owner_id=user_id)

        # 각 restaurant에 대해 카테고리와 소유주 이름 가져오기
        restaurant_data = []
        for restaurant in restaurants:
            categories = restaurant.categories.all()  # 해당 가게에 연결된 모든 카테고리 쿼리셋을 가져옴
            category_names = [category.name for category in categories]  # 카테고리 이름 목록
            
            # owner의 username 가져오기
            owner_username = restaurant.owner.username  # 소유자의 username

            restaurant_data.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'description': restaurant.description,
                'image_url': restaurant.image_url,
                'categories': category_names,
                'owner': owner_username,
                'address': restaurant.address,
                'phone_number': restaurant.phone_number,
                'operating_hours': restaurant.operating_hours,
                'rating': restaurant.rating,
                'delivery_fee': restaurant.delivery_fee
            })
        
        # 직렬화된 데이터를 JSON으로 응답
        return Response(restaurant_data, status=status.HTTP_200_OK)
    except Restaurant.DoesNotExist:
        return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
    



# 가게 정보 수정
@api_view(['PUT'])
def update_store(request, store_id):
    try:
        store = Restaurant.objects.get(id=store_id)

        # 요청 데이터에서 가게 정보 가져오기
        name = request.data.get('name', store.name)
        phone_number = request.data.get('phone_number', store.phone_number)  
        address = request.data.get('address', store.address) 
        description = request.data.get('description', store.description) 
        operating_hours = request.data.get('operating_hours', store.operating_hours) 
        rating = request.data.get('rating', store.rating) 
        delivery_fee = request.data.get('delivery_fee', store.delivery_fee)

        # 이미지 업데이트
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            fs = FileSystemStorage() 
            # 이미지 파일 저잗하고 파일 경로 가져오기
            filename = fs.save(f'images/{image_file.name}', image_file)
            store.image = filename  # 이미지 필드에 파일 이름 저장
            store.image_url = f"{request.build_absolute_uri('/media/')}{filename}"  # 이미지 URL 저장


        # 모든 필드들 업데이트
        store.name = name
        store.phone_number = phone_number
        store.address = address
        store.description = description
        store.operating_hours = operating_hours
        store.rating = rating
        store.delivery_fee = delivery_fee

        store.save()

        return Response({
            'message': '가게 정보가 업데이트되었습니다.',
            'store': {
                'name': name,
                'phone_number': phone_number,
                'description': description,
                'address': address,
                'operating_hours': operating_hours,
                'rating': rating,
                'delivery_fee': delivery_fee,
                'image_url': store.image_url if store.image else None
            }
        }, status=status.HTTP_200_OK)

        

    except Restaurant.DoesNotExist:
        return Response({'error': '가게를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print(f"Error: {str(e)}")  # 에러 로그 출력
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# 가게 삭제 뷰
def delete_store(request, store_id):
    try:
        store = get_object_or_404(Restaurant, id=store_id)
        store.delete()  # 가게 삭제
        return JsonResponse({'message': '가게가 성공적으로 삭제되었습니다.'}, status=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    


# 메뉴 등록 뷰
@api_view(['POST'])
def create_menu(request, store_id):
    try:
        if request.method == 'POST':
            # 요청 데이터에서 메뉴 정보 추출
            menu_data = request.data.copy()
            print('메뉴 데이터', menu_data)

            # options 데이터 가져오기 및 JSON 파싱
            options_str = menu_data.get('options', None)
            if options_str:
                try:
                    options = json.loads(options_str)
                    print('파싱된 options', options)
                    menu_data['options'] = options
                except json.JSONDecodeError as e:
                    print('JSON 파싱 오류', str(e))
                    return Response({'error': 'Invalid JSON format for options'}, status=status.HTTP_400_BAD_REQUEST)
            
            print('최종 menu_data', menu_data)
            
            # MenuSerializer를 사용하여 데이터 유효성 검사
            menu_serializer = MenuSerializer(data=menu_data)

            if menu_serializer.is_valid():
                # 메뉴 저장 (store_id를 restaurant_id로 사용)
                print('메뉴 저장 중...')
                menu = menu_serializer.save(restaurant_id=store_id)
                print('메뉴 저장 완료')

                # 이미지 파일이 있을 경우 저장
                print('이미지 저장')
                if 'image' in request.FILES:
                    image_file = request.FILES['image']
                    fs = FileSystemStorage()
                    # 이미지 파일 저장하고 파일 경로 가져오기
                    filename = fs.save(f'menus/{image_file.name}', image_file)
                    menu.image = filename  # 이미지 필드에 파일 이름 저장
                    menu.image_url = f"{request.build_absolute_uri('/media/')}{filename}"  # 이미지 URL 저장
                    menu.save() # menu 객체 업데이트
                    print('이미지 저장하고 menu 저장')

                return Response(menu_serializer.data, status=status.HTTP_201_CREATED)  # 성공적으로 저장된 메뉴 반환
            else:
                print(menu_serializer.errors)  # 유효성 검사 오류 출력
                return Response(menu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 유효성 검사 실패 시 오류 반환

    except Exception as e:
        print(f"Error: {str(e)}")  # 에러 로그 출력
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 가게 메뉴 조회 뷰
@api_view(['GET'])
def store_menu_view(request, store_id):
    menus = Menu.objects.filter(restaurant_id=store_id)

    if not menus.exists():
        # 메뉴가 없을 경우 404 반환
        return Response({"error": "No matching records found"}, status=status.HTTP_404_NOT_FOUND)
    
    menus_data = []

    for menu in menus:
        # 메뉴에 해당하는 옵션 그룹 조회
        optiongroups = OptionGroup.objects.filter(menu=menu)

        # 각 옵션 그룹에 대한 옵션 아이템들 조회
        optiongroups_data = []

        for optiongroup in optiongroups:
            optionitems = OptionItem.objects.filter(group=optiongroup)

            optionitems_data = []
            for optionitem in optionitems:
                optionitems_data.append({
                    'name': optionitem.name,
                    'price': optionitem.price
                })

            optiongroups_data.append({
                'group_name': optiongroup.name,
                'items': optionitems_data
            })

        #print(f"optiongroups_data for menu {menu.id}: {optiongroups_data}")
        
        # 메뉴 데이터와 옵션 그룹 데이터를 menus_data에 추가
        menus_data.append({
            'id': menu.id,
            'name': menu.name,
            'description': menu.description,
            'price': menu.price,
            'image_url': menu.image_url,
            'option_groups': optiongroups_data
        })
    
    return Response(menus_data, status=status.HTTP_200_OK)



        