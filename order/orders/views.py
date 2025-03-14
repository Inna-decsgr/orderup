from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import UserProfile, Restaurant, Order, OrderItem, OrderItemOption, Menu, Category, Like
from rest_framework import status
from orders.models import UserProfile, Menu, OptionGroup, OptionItem, Rider, Review, Coupon, UserCoupon
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from .serializers import RestaurantSerializer, RiderSerializer
from rest_framework import generics
from decimal import Decimal, InvalidOperation
from django.core.files.storage import FileSystemStorage
from .serializers import MenuSerializer 
import json
from django.db import transaction
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the home page!")


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
        owner = request.data.get('owner')
        operating_hours = request.data.get('operating_hours', None)
        description = request.data.get('description')
        delivery_fee = request.data.get('delivery_fee', 500.0)
        image_file = request.FILES.get('image', None)
        image_url = request.data.get('image_url', None)  # ✅ 기존 URL 값도 받아오기

        # ✅ categories를 JSON 문자열에서 리스트로 변환
        categories = request.data.get('categories', "[]")
        try:
            category_ids = json.loads(categories)
            if not isinstance(category_ids, list):
                raise ValueError("categories 필드는 리스트여야 합니다.")
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format for categories'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        print("Received image_url:", phone_number)
        # 새로운 Restaurant 객체 생성
        restaurant = Restaurant(
            name=name,
            address=address,
            phone_number=phone_number,
            rating=rating,
            owner_id=owner,
            operating_hours=operating_hours,
            description=description,
            delivery_fee=delivery_fee,
            image_url=image_url  # ✅ 기존 URL 저장
        )

        # ✅ 이미지 파일이 있을 경우 업로드 및 URL 저장
        if image_file:
            restaurant.image = image_file
            restaurant.image_url = f"{request.build_absolute_uri(restaurant.image.url)}"  # ✅ 이미지 URL 저장

        restaurant.save()
        restaurant.categories.set(category_ids)

        serializer = RestaurantSerializer(restaurant, context={'request': request})  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        



# 가게 소유쥬 id로 가게 정보 조회하는 뷰
@api_view(['GET'])
def my_store_view(request, user_id):
    try:
        # owner_id가 user_id와 일치하는 레코드 조회
        restaurants = Restaurant.objects.filter(owner_id=user_id)

        # 각 restaurant에 대해 카테고리와 소유주 이름 가져오기
        restaurant_data = []
        for restaurant in restaurants:
            categories = restaurant.categories.all()  # 해당 가게에 연결된 모든 카테고리 쿼리셋을 가져옴
            reviews = restaurant.reviews.count()
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
                'delivery_fee': restaurant.delivery_fee,
                'reviews': reviews
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


# 메뉴 조회 뷰
@api_view(['GET'])
def store_menu_view(request, store_id):
    try:
        menus = Menu.objects.filter(restaurant_id=store_id)

        if not menus.exists():
            # 메뉴가 없을 경우 404 반환
            return Response({"message": "등록된 메뉴가 없습니다"}, status=status.HTTP_200_OK)
    
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
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 로그로 출력
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 메뉴 삭제하는 뷰
def delete_menu(request, menu_id):
    try:
        menu = get_object_or_404(Menu, id=menu_id)
        menu.delete()  # 가게 삭제
        return JsonResponse({'message': '가게가 성공적으로 삭제되었습니다.'}, status=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)


# 메뉴 수정 뷰
@api_view(['PUT'])
def update_menu(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id)

        # 요청 데이터에서 메뉴 정보 가져오기
        name = request.data.get('name', menu.name)
        description = request.data.get('description', menu.description)
        price = request.data.get('price', menu.price)

        # 이미지 업데이트
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            # 이미지 파일 저장하고 파일 경로 가져오기
            filename = fs.save(f'menus/{image_file.name}', image_file)
            menu.image = filename
            menu.image_url = f"{request.build_absolute_uri('/media/')}{filename}"

        # 모든 필드들 업데이트
        menu.name = name
        menu.description = description
        menu.price = price

        menu.save()

        return Response({
            'message' : '메뉴 정보가 업데이트 되었습니다.',
            'menu': {
                'name': name,
                'description': description,
                'price': price,
                'image_url': menu.image_url if menu.image else None
            }
        }, status=status.HTTP_200_OK)
    
    except Menu.DoesNotExist:
        return Response({'error': '메뉴를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# 모든 가게 정보 조회하기
@api_view(['GET'])
def get_all_stores(request):
    # category 쿼리 파라미터 가져오기
    stores = Restaurant.objects.all()
    
    stores_data = []

    for store in stores:
        menus = Menu.objects.filter(restaurant_id=store.id)

        stores_data.append({
            'id': store.id,
            'name': store.name,
            'address': store.address,
            'phonenumber': store.phone_number,
            'rating': store.rating,
            'description': store.description,
            'deliveryfee': store.delivery_fee,
            'operatinghours': store.operating_hours,
            'imageurl': store.image_url,
            'categories': [category.name for category in store.categories.all()],  # 카테고리 리스트 추가
            'reviews': [
                {
                    'id': review.id,
                    'user': review.user.username,  # 유저 이름 추가
                    'rating': review.rating,
                    'content': review.content,
                    'date': review.date,
                    'imageurl': review.image_url,
                }
                for review in store.reviews.all()  # Menu와 리뷰 연결된 경우
            ],

            'menus': [
                {
                    'id': menu.id,
                    'name': menu.name,
                    'description': menu.description,
                    'price': menu.price,
                    'imageurl': menu.image_url,
                }
                for menu in menus.all()
            ]
        })

    return Response(stores_data, status=status.HTTP_200_OK)



# 새로운 주문 추가하기
@api_view(['POST'])
def add_new_order(request):
    """
    결제 정보를 받아서 주문을 처리하고 저장하는 API 뷰
    """
    # 요청 데이터에서 주문과 결제 정보 추출
    order_data = request.data.get('items')
    payment_details = request.data.get('paymentDetails')
    total_amount = request.data.get('totalAmount')
    restaurant_id = request.data.get('restaurant_id')
    user_coupon_id = request.data.get('user_coupon_id')
    discount_amount = request.data.get('discount_amount')


    if restaurant_id:
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            delivery_fee = restaurant.delivery_fee or 0
        except Restaurant.DoesNotExist:
            return Response({'error': '레스토랑을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': '레스토랑 ID가 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    
    user_coupon = None
    if user_coupon_id:
        print(restaurant_id)
        print(user_coupon_id)
        try:
            user_profile = UserProfile.objects.get(user_id=user_coupon_id)
            print(user_profile)
            user_coupon = UserCoupon.objects.get(store_id=restaurant_id, user_profile_id=user_profile.id, is_used=False)
        except UserCoupon.DoesNotExist:
            return Response({'error': '해당 쿠폰 정보를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


    # 트랜잭션을 이용하여 여러 DB 작업을 하나의 단위로 처리
    try:
        with transaction.atomic():
            # 주문 생성
            order = Order.objects.create(
                user=request.user,  # 로그인된 사용자
                restaurant=restaurant,
                total_price=total_amount,
                status='pending',
                payment_method='카드 결제', 
                payment_details=payment_details,
                user_coupon_id=user_coupon.id if user_coupon else None,
                discount_amount=discount_amount if discount_amount else None,
            )

            # 쿠폰 적용 시 최종 가격 계산
            if user_coupon:
                final_price = max(0, total_amount - discount_amount + delivery_fee)
                order.final_price = final_price
                order.save()

                user_coupon.is_used = True
                user_coupon.used_at = timezone.now()
                user_coupon.save()


            # 주문 항목 저장
            for item_data in order_data:
                try:
                    menu = Menu.objects.get(id=item_data['menu_id'])
                except Menu.DoesNotExist:
                    return Response({'error': f"메뉴 ID {item_data['menu_id']}에 해당하는 메뉴가 없습니다."},
                                    status=status.HTTP_404_NOT_FOUND)

                order_item = OrderItem.objects.create(
                    order=order,
                    menu=menu,
                    quantity=1  # 기본 수량 1로 설정 (필요시 수정 가능)
                )

                # 옵션 처리
                if item_data['options']:  # 옵션이 존재하는 경우에만 처리
                    for option in item_data['options']:
                        # option이 배열로 되어 있다면, 그 안에서 추가 처리
                        if isinstance(option, dict):  # 옵션이 딕셔너리 형태일 경우
                            OrderItemOption.objects.create(
                                order_item=order_item,
                                name=option['name'],
                                price=option['price']
                            )
                        else:
                            return Response({'error': '옵션 데이터가 잘못된 형식입니다.'},status=status.HTTP_400_BAD_REQUEST)
                        
            response_data = {
                'message': '주문이 성공적으로 처리되었습니다.',
                'order_id': order.id,
                'final_price': order.final_price,
                'discount_applied': user_coupon.coupon.discount_amount if user_coupon else 0,
                'coupon_used': user_coupon_id if user_coupon else None
            }

            # 성공적으로 주문을 처리한 후 응답
            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # 예외 처리 (예: 트랜잭션 실패)
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

# 사용자 id에 맞게 주문 내역 가져오기
@api_view(['GET'])
def get_order_list(request, user_id):
    try:
        # user_id가 일치하는 주문 조회
        orders = Order.objects.filter(user_id=user_id)
        
        # 주문 데이터 저장할 리스트
        order_data = []
        for order in orders:
            order_items = []
            for item in order.items.all():
                # 각 OrderItem과 연결된 Menu 정보
                menu = {
                    "menu_id": item.menu.id,
                    "name": item.menu.name,
                    "description": item.menu.description,
                    "price": item.menu.price,
                    "image_url": item.menu.image_url
                }

                # 각 OrderItem과 연결된 OrderItemOption 정보
                options = [
                    {
                        "name": option.name,
                        "price": option.price 
                    }
                    for option in item.options.all()
                ]

                # OrderItem 정보를 추가
                order_items.append({
                    "order_item_id" : item.id,
                    "quantity" : item.quantity,
                    "menu" : menu,
                    "options" : options
                })

            # 주문 정보를 추가
            order_data.append({
                "order_id" : order.id,
                "restaurant": {
                    "id": order.restaurant_id,
                    "name": order.restaurant.name,
                    "address" : order.restaurant.address,
                    "phone_number" : order.restaurant.phone_number,
                    "deliveryfee" : order.restaurant.delivery_fee,
                    "rating": order.restaurant.rating,
                    "description": order.restaurant.description,
                    'image_url': order.restaurant.image_url
                },
                "ordered_at": order.ordered_at,
                "status" : order.status,
                "total_price": order.total_price,
                "payment_method" : order.payment_method,
                "payment_details" : order.payment_details,
                "items" : order_items,
                "review": order.review,
                "discount_amount": order.discount_amount
            })

        return Response(order_data)
        
    except Order.DoesNotExist:
        return Response({"error": "No orders found for this user"}, status=404)


# 주문 취소하면 해당 주문 상태를 pending에서 canceled로 변경하기
@api_view(['PUT'])
def cancel_order(request, order_id):
    try:
        print(order_id)
        # Order 객체 가져오기
        order = Order.objects.get(id=order_id)
        print('주문취소할 주문', order)

        order.status = 'canceled'

        order.save()

        return JsonResponse({'message': '주문이 취소되었습니다.', 'order_id': order.id}, status=200)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': '주문을 찾을 수 없습니다.'}, status=404)



# 주문 데이터 생성 함수
from .models import OrderChart
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.utils import timezone 
import random

def generate_fake_orders(n=100):
    menu_ids = list(range(38, 109))
    store_ids = list(range(5, 20))
    user_ids = [2, 8, 9, 13, 15]

    now = timezone.now()  # timezone.now()로 현재 시간 가져오기
    orders = []

    for _ in range(n):
        # 각 주문마다 랜덤한 날짜를 생성 (최근 7일 내의 날짜)
        random_days = random.randint(0, 7)  # 0부터 7일 사이의 랜덤 숫자
        order_date = now - timedelta(days=random_days)  # 랜덤한 날짜 생성

        order = OrderChart(
            store_id=random.choice(store_ids),
            menu_id=random.choice(menu_ids),
            user_id=random.choice(user_ids),
            order_date=order_date,  # 최근 7일 데이터
        )
        orders.append(order)

    # 한꺼번에 저장
    print(f"Generated {len(orders)} orders")  # 추가된 로깅
    OrderChart.objects.bulk_create(orders)
    print(f"Saved {len(orders)} orders to the database.")  # 저장된 주문 수 로깅

def create_order_data(request):
    generate_fake_orders(1000)  # 200개의 데이터 생성
    orders_count = OrderChart.objects.count()  # 데이터베이스에 저장된 주문 수 확인
    return JsonResponse({"message": f"Fake order data generated successfully! {orders_count} orders created."})


import logging
logger = logging.getLogger(__name__)
# 차트 데이터 반환 함수
def get_popular_menu(request):
    try:
        # 최근 3일 간의 주문 데이터를 가져오기
        one_year_ago = timezone.now() - timedelta(days=365)

        menu_counts = (
            OrderChart.objects.filter(order_date__gte=one_year_ago)  # 최근 1년간 데이터 필터링
            .values("menu_id")
            .annotate(count=Count("menu_id"))
            .order_by("-count")
        )

        #print("Menu counts:", menu_counts)  # 쿼리 결과 출력

        # 상위 8개 메뉴에 대해 메뉴 이름과 주문량을 반환
        labels = []
        data = []
        for item in menu_counts[:8]:
            try:
                menu = Menu.objects.get(id=item["menu_id"])
                labels.append(menu.name)
                data.append(item["count"])
            except Menu.DoesNotExist:
                labels.append("Unknown")
                data.append(item["count"])

        # 서버 측에서 반환되는 데이터 확인
        #print("Chart Data:", {"labels": labels, "data": data})  # 로그로 확인

        # 차트 데이터 반환
        chart_data = {"labels": labels, "data": data}
    
        return JsonResponse(chart_data)
    except Exception as e:
        logger.error(f"Error in popular_menu: {str(e)}")  # 로그 기록
        return JsonResponse({'error': str(e)}, status=500)



# 주문 관리 페이지에서 새로 들어온 주문 사업자, 가게에 맞게 들고오기
@api_view(['GET'])
def get_new_order(request, store_id):
    try:
        orders = Order.objects.filter(restaurant_id=store_id)
        store = Restaurant.objects.get(id=store_id)

        # 주문 항목과 옵션도 포함해서 데이터 가져오기
        order_data = []
        for order in orders:
            # OrderItem과 OrderItemOption 데이터를 포함시켜서 가져옴
            items = OrderItem.objects.filter(order=order)
            order_items = []
            for item in items:
                options = OrderItemOption.objects.filter(order_item=item)
                order_items.append({
                    'item' : item.menu.name,
                    'price' : item.menu.price,
                    'quantity' : item.quantity,
                    'options' : [{ 'name' : option.name, 'price' : option.price} for option in options]
                })

            # 사용자 정보 가져오기
            try:
                user_profile = UserProfile.objects.get(user=order.user)
                user_phone = user_profile.phone_number
                user_address = user_profile.address
            except UserProfile.DoesNotExist:
                user_phone = None
                user_address = None

            #  주문 데이터와 항목, 옵션들 포함
            order_data.append({
                'order_id' : order.id,
                'user': order.user.username,
                'user_phone' : user_phone,
                'user_address' : user_address,
                'ordered_at' : order.ordered_at,
                'status' : order.status,
                'total_price' : str(order.total_price),
                'payment_method' : order.payment_method,
                'order_items' : order_items,
                'discount_amount': str(order.discount_amount) if order.discount_amount else "0.00",
                'final_price' : order.final_price,
                'user_coupon_id': order.user_coupon.id if order.user_coupon else None,
                'delivery_fee' : store.delivery_fee
            })

        return Response({'orders' : order_data})



    except Order.DoesNotExist:
        return Response({'error': "No orders found for this user"}, status=404)
    

# 주문 수락하면 해당 주문 상태를 pending에서 accepted로 변경하기
@api_view(['PUT'])
def accept_order(request, order_id):
    try:
        print(order_id)
        # Order 객체 가져오기
        order = Order.objects.get(id=order_id)
        order.status = 'accepted'
        order.save()

        return JsonResponse({'message': '주문이 수락되었습니다.', 'order_id': order.id}, status=200)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': '주문을 찾을 수 없습니다.'}, status=404)


# 주문 거절하면 해당 주문 상태를 pending에서 rejected로 변경하기
@api_view(['PUT'])
def reject_order(request, order_id):
    try:
        print(order_id)
        # Order 객체 가져오기
        order = Order.objects.get(id=order_id)
        order.status = 'rejected'
        order.save()

        return JsonResponse({'message': '주문이 거절되었습니다.', 'order_id': order.id}, status=200)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': '주문을 찾을 수 없습니다.'}, status=404)
    


# 배달 픽업하면 해당 주문 상태를 accepted에서 delivering으로 변경하기
@api_view(['PUT'])
def delivering_order(request, order_id):
    try:
        print(order_id)
        # Order 객체 가져오기
        order = Order.objects.get(id=order_id)
        order.status = 'delivering'
        order.save()

        return JsonResponse({'message': '배달원이 음식을 픽업하고 배달중입니다.', 'order_id': order.id}, status=200)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': '주문을 찾을 수 없습니다.'}, status=404)



# 해당 가게에 새로 들어온 주문 갯수 가져오기
@api_view(['GET'])
def get_order_length(request, store_id):
    orders = Order.objects.filter(restaurant_id=store_id, status='pending')

    order_count = orders.count()

    return JsonResponse({'order_count': order_count})


# 배달 라이더 정보 가져오기
@api_view(['GET'])
def get_rider_info(request):
    riders = Rider.objects.all()
    serializer = RiderSerializer(riders, many=True)
    return JsonResponse({"rider_info": serializer.data})


# 배달이 완료되면 해당 주문 상태를 delivering에서 delivered로 변경하기
@api_view(['PUT'])
def completed_delivery(request, order_id):
    try:
        print(order_id)
        # Order 객체 가져오기
        order = Order.objects.get(id=order_id)
        order.status = 'delivered'
        order.save()

        return JsonResponse({'message': '배달이 완료되었습니다.', 'order_id': order.id}, status=200)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': '배달 중 오류가 발생했습니다.'}, status=404)
    

# 새 리뷰 등록하기
@api_view(['POST'])
def register_review(request, store_id):
    if request.method == 'POST':

        print(request.data)

        try:
            #요청 데이터에서 메뉴 정보 추출
            rating = request.POST.get("rating")
            review_content = request.POST.get("review")
            user_id = request.POST.get("userid")
            order_id= request.POST.get("orderid")
            
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
            
            # 가게 객체 가져오기
            store = get_object_or_404(Restaurant, pk=store_id)

            # 해당 주문 가져오기
            try:
                order = Order.objects.get(pk=order_id, user=user, restaurant=store)
            except Order.DoesNotExist:
                return JsonResponse({"error": "Order not found or does not match user/store"}, status=404)

            # 리뷰 생성
            review = Review(
                user_id=user.id,
                store=store,
                rating=rating,
                content=review_content,
                date=timezone.now(),
                order_id=order_id
            )

            # 이미지 저장
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                fs = FileSystemStorage()
                # 이미지 파일 저장
                filename = fs.save(f'reviews/{image_file.name}', image_file)
                review.image = filename 
                review.image_url = f"{request.build_absolute_uri('/media/')}{filename}"  

            review.save()

            # 해당 주문의 review 필드 True로 업데이트
            order.review = True
            order.save()

            # JSON 응답을 위해 이미지 필드를 문자열로 변환
            image_url = review.image.url if review.image else None

            return JsonResponse({
                "message": "Review successfully created",
                "review_id": review.id,
                "order_id": review.order_id,
                "user": user.id,
                "store": store.id,
                "rating": review.rating,
                "content": review.content,
                "date": review.date,
                "image": image_url,
                "image_url": review.image_url
            }, status=201)
        
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"},  status=500)


# 해당 가게의 리뷰 모두 가져오기
@api_view(['GET'])
def get_all_reviews(request, store_id):
    try:
        # 특정 가게 가져오기
        store = Restaurant.objects.get(id=store_id)

        # 해당 가게의 모든 리뷰 가져오기
        reviews = store.reviews.select_related('user')
        print(reviews)

        # 리뷰 정보 담을 리스트 생성
        reviews_data = []
        for review in reviews:
            menus = []
            if review.order:
                order_items = review.order.items.select_related('menu')
                menus = [{
                    'menu_id': item.menu.id, 
                    'name': item.menu.name, 
                    'quantity': item.quantity} 
                    for item in order_items
                ]

            review_data = {
                'review_id': review.id,
                'rating': review.rating,
                'content': review.content,
                'date': review.date,
                'image_url': review.image_url,
                'user' : {
                    'id' : review.user.id,
                    'username': review.user.username
                },
                'menus': menus
            }
            reviews_data.append(review_data)

        return JsonResponse({'store_id': store.id, 'reviews': reviews_data}, safe=False)
    
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': '가게를 찾을 수 없습니다.'}, status=404)


# 리뷰 삭제하는 뷰
def remove_reviews(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        review.delete()  # 리뷰 삭제
        return JsonResponse({'message': '리뷰가 성공적으로 삭제되었습니다.'}, status=204)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    


# 내가 작성한 리뷰 불러오기
@api_view(['GET'])
def get_my_review(request):
    userid = request.GET.get('userid')
    storeid = request.GET.get('storeid')

    # Review 테이블에서 조건에 맞는 리뷰 가져오기
    reviews = Review.objects.filter(user_id=userid, store_id=storeid).select_related('user')

    review_list = []
    for review in reviews:
        # 주문 정보 가져오기 (리뷰와 연결된 주문)
        order = review.order

        # 주문한 메뉴 가져오기 (OrderItem에서 조회)
        order_items = OrderItem.objects.filter(order=order).select_related('menu')

        # 메뉴 리스트 만들기
        items_data = [
            {
                "menu_id": item.menu.id,
                "menu_name": item.menu.name,
                "quantity": item.quantity,
                "price": float(item.menu.price),
            }
            for item in order_items
        ]

        review_list.append({
            "id": review.id,
            "content": review.content,
            "rating": review.rating,
            "username": review.user.username,
            "date": review.date.strftime("%Y-%m-%d %H:%M:%S"),  # 날짜 포맷
            "image_url": review.image_url,
            "order_id": order.id if order else None,  # 주문 ID 추가
            "items": items_data,  # 주문한 메뉴 추가
        })

    return JsonResponse({"reviews": review_list})


# 리뷰 수정하는 뷰 함수
@api_view(['PUT'])
def edit_my_review(request, review_id):
    try:
        print(review_id)
        # 리뷰 객체 가져오기
        review = Review.objects.get(id=review_id)

        # 요청에서 전달받은 데이터 처리
        content = request.data.get('content')
        rating = request.data.get('rating')

        if 'image' in request.FILES:
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(f'reviews/{image_file.name}', image_file)
            review.image = filename
            review.image_url = f"{request.build_absolute_uri('/media/')}{filename}"

        # 수정된 내용 반영
        review.content = content
        review.rating = rating

        review.save()

        return JsonResponse({'message': '리뷰를 성공적으로 수정하였습니다.', 'review_id': review.id}, status=200)
    
    except Review.DoesNotExist:
        return JsonResponse({'error': '리뷰를 찾을 수 없습니다.'}, status=404)

# 가게 찜하기
@api_view(['POST'])
def toggle_like(request, user_id):
        try:
            user = User.objects.get(id=user_id)
            store_id = request.data.get("storeid")

            # Like가 이미 존재하는지 확인
            like, created = Like.objects.get_or_create(user=user, store_id=store_id)

            if not created:
                # 이미 존재하면 is_active 상태를 반전시키기
                like.is_active = not like.is_active
            else:
                # 새로 생성된 경우 is_active를 true로 설정
                like.is_active = True
                like.created_at = timezone.now()

            like.save()
            print(like.is_active)
            return JsonResponse({'is_active': like.is_active}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': '유저를 찾을 수 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



# 가게들 찜 정보 불러오기
@api_view(['GET'])
def get_store_likes(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        # Like 모델에서 해당 유저가 찜한 정보를 추출하기
        likes = Like.objects.filter(user=user, is_active=True).select_related('store')

        # 유저가 찜한 가게의 정보를 JSON 형태로 반환
        store_likes = [
            {
                'store_id' : like.store.id,
                'store_name' : like.store.name,
                'rating' : like.store.rating,
                'review_count': like.store.reviews.count(),
                'delivery_fee' : float(like.store.delivery_fee),
                'description' : like.store.description,
                'image' : like.store.image.url if like.store.image else None,
                'image_url' : like.store.image_url,
                'created_at' : like.created_at,
                'is_active' : like.is_active,
                'operatinghours' : like.store.operating_hours
            }
            for like in likes
        ]

        return JsonResponse({'likes': store_likes}, safe=False)
    
    except User.DoesNotExist:
            return JsonResponse({'error': '유저를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



# 쿠폰 발급하는 뷰
@api_view(['POST'])
def get_store_coupon(request, user_id):
    try:
        # 요청에서 storeid랑 discount_amount 가져오기
        data = request.data
        store_id = data.get('storeid')
        discount_amount = data.get('discount_amount')

        # 사용자 프로필과 가게 정보 가져오기
        user_profile = UserProfile.objects.get(user_id=user_id)
        store = Restaurant.objects.get(id=store_id)

        # 유효한 쿠폰이 있는지 확인하기
        coupon, created = Coupon.objects.get_or_create(
            code=f'FIRST{discount_amount}',  # 쿠폰 코드 예시
            defaults={'discount_amount': discount_amount, 'is_active': True}
        )
        
        if coupon.is_active:
            # UserCoupon 모델에 새 쿠폰 발급
            user_coupon = UserCoupon.objects.create(
                user_profile=user_profile,
                coupon = coupon,
                store=store,
                is_used=False
            )

            return JsonResponse({
                "message": "쿠폰이 발급되었습니다.",
                "coupon_code": coupon.code,
                "discount_amount": coupon.discount_amount,
                "store": store.name,
                'user_coupon_id': user_coupon.id
            }, status=200)
        else:
            return JsonResponse({"error": "유효하지 않은 쿠폰입니다."}, status=400)

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "사용자를 찾을 수 없습니다."}, status=404)
    except Restaurant.DoesNotExist:
        return JsonResponse({"error": "가게를 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    



# 사용자가 발급받은 모든 쿠폰 가져오기
@api_view(['GET'])
def get_all_coupons(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)

        # 해당 사용자가 발급받은 모든 쿠폰 조회
        coupons = UserCoupon.objects.filter(user_profile=user_profile)

        # 직렬화된 쿠폰 데이터 생성
        coupon_data = [
            {
                'coupon_code': coupon.coupon.code,
                'is_used': coupon.is_used,
                'store_id': coupon.store.id if coupon.store else None,
                'store': coupon.store.name if coupon.store else None,
                'created_at': coupon.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'discount_amount': f"{coupon.coupon.discount_amount:.0f}",
                'expired_date': (coupon.created_at + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
            }
            for coupon in coupons
        ]

        return JsonResponse({'coupons': coupon_data}, safe=False)
    
    except UserProfile.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



# 사용자가 작성한 리뷰 모두 가져오기
@api_view(['GET'])
def get_all_user_reviews(request, user_id):
    try:
        # 특정 가게 가져오기
        user = User.objects.get(id=user_id)

        # 해당 가게의 모든 리뷰 가져오기
        reviews = user.reviews.all().select_related('user')

        if not reviews.exists():
            return JsonResponse({'user_id': user.id, 'reviews': [], 'message': '리뷰가 없습니다.'}, status=200)
        print(reviews)

        # 리뷰 정보 담을 리스트 생성
        reviews_data = []
        for review in reviews:
            review_data = {
                'review_id': review.id,
                'rating': review.rating,
                'content': review.content,
                'date': review.date,
                'image_url': review.image_url,
                'user' : {
                    'id' : review.user.id,
                    'username': review.user.username
                },
                'store': {
                    'store_id': review.store.id,
                    'store_name': review.store.name, 
                    'store_address': review.store.address
                }
            }
            reviews_data.append(review_data)

        return JsonResponse({'user_id': user.id, 'reviews': reviews_data}, safe=False)
    
    except User.DoesNotExist:
        return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
    



# 찜된 모든 가게들 가져오기
@api_view(['GET'])
def get_all_liked_stores(request):
    try:
        # 찜된 가게 모두 가져오기
        popular_stores = (
            Like.objects.filter(is_active=True)
            .values('store_id')
            .annotate(like_count=Count('id'))
            .filter(like_count__gte=2)
            .order_by('-like_count')
        )

        # 리뷰 정보 담을 리스트 생성
        liked_all_stores = []
        for store in popular_stores:
            store_instance = Restaurant.objects.get(id=store['store_id'])

            liked_store_data = {
                'store': {
                    'id': store_instance.id,
                    'name': store_instance.name, 
                    'address': store_instance.address,
                    'rating' : store_instance.rating,
                    'delivery_fee' : store_instance.delivery_fee,
                    'image_url' : store_instance.image_url,
                    'like_count': store['like_count']
                }
            }
            liked_all_stores.append(liked_store_data)

        return JsonResponse({'liked_stores': liked_all_stores}, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': 'str(e)'}, status=500)



# 검색 키워드를 포함하고 있는 메뉴의 가게 정보 반환
@api_view(['GET'])
def get_all_menus(request, keyword): 
    if not keyword:
        return Response({"error": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 메뉴 이름에 keyword가 포함된 메뉴 필터링
    menus = Menu.objects.filter(name__icontains=keyword)

    # 필터링된 메뉴의 가게 정보 포함
    menu_data = [
        {
            'menu_id': menu.id,
            'menu_name': menu.name,
            'menu_description': menu.description,
            'menu_price': menu.price,
            'menu_imageurl': menu.image_url,
            'restaurant': {
                'id': menu.restaurant.id,
                'name': menu.restaurant.name,
                'address': menu.restaurant.address,
                'phonenumber': menu.restaurant.phone_number,
                'rating': menu.restaurant.rating,
                'description': menu.restaurant.description,
                'deliveryfee': menu.restaurant.delivery_fee,
                'operatinghours': menu.restaurant.operating_hours,
                'imageurl': menu.restaurant.image_url,
                'categories': [category.name for category in menu.restaurant.categories.all()],
                'reviews': [
                    {
                        'user': review.user.username,
                        'rating': review.rating,
                        'date': review.date,
                        'content': review.content,
                        'image_url': review.image_url
                    }
                    for review in menu.restaurant.reviews.all()
                ],
            }
        }
        for menu in menus
    ]

    return Response(menu_data, status=status.HTTP_200_OK)




# 주문 상세 데이터 불러오기
@api_view(['GET'])
def get_order_detail(request, orderid):
    try:
        # orderid에 해당하는 주문 가져오기
        order = Order.objects.get(id=orderid)
        
        # 가게 정보 가져오기
        restaurant = order.restaurant
        delivery_fee = float(restaurant.delivery_fee)

        # 주문한 메뉴 정보 가져오기
        order_items = OrderItem.objects.filter(order=order)

        # 주문한 메뉴 리스트 만들기
        items_data = []
        for item in order_items:
            # 해당 주문 아이템의 옵션 가져오기
            options = OrderItemOption.objects.filter(order_item=item)
            options_data = [
                {"name": option.name, "price": float(option.price)}
                for option in options
            ]

            items_data.append({
                "menu_id": item.menu.id,
                "menu_name": item.menu.name,
                "quantity": item.quantity,
                'price': item.menu.price,
                "options": options_data,  # 옵션 추가
            })

        # 주문 데이터를 딕셔너리 형태로 변환해서 반환
        order_data = {
            "id": order.id,
            "user": order.user.id,  # User 모델의 ID
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "delivery_fee": delivery_fee  # 배달료 추가
            },
            "ordered_at": order.ordered_at.strftime("%Y-%m-%d %H:%M:%S"),  # 날짜 포맷팅
            "status": order.status,
            "total_price": float(order.total_price),  # Decimal을 float으로 변환
            "payment_method": order.payment_method,
            "payment_details": order.payment_details,  # JSONField는 그대로 반환 가능
            "review": order.review,
            "user_coupon": order.user_coupon.id if order.user_coupon else None,  # ForeignKey 값 확인
            "discount_amount": float(order.discount_amount) if order.discount_amount else 0.0,
            "final_price": float(order.final_price) if order.final_price else 0.0,
            "items": items_data,  # 주문한 메뉴 정보 추가
        }

        return Response(order_data, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


