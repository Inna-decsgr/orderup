from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import home, login_view, signup_view, update_user, get_user, delete_user, csrf_token_view, store_regis, my_store_view, update_store, delete_store, create_menu, store_menu_view, delete_menu, update_menu, get_all_stores, add_new_order, get_order_list, cancel_order, create_order_data, get_popular_menu, get_new_order, accept_order, reject_order, get_order_length, get_rider_info, delivering_order, completed_delivery, register_review, get_all_reviews, remove_reviews, get_my_review, edit_my_review, toggle_like, get_store_likes, get_store_coupon, get_all_coupons, get_all_user_reviews, get_all_liked_stores, get_all_menus, get_order_detail

urlpatterns = [
    path('', home, name='home'), 
    path('signup/', signup_view, name='signup'),  # 회원가입 URL
    path('login/', login_view, name='login'),  # 로그인 URL
    path('edituser/<int:user_id>/', update_user, name='edituser'), # 사용자 정보 수정 URL
    path('getuser/<int:user_id>/', get_user, name='getuser'), # 사용자 정보 조회 URL
    path('deleteuser/<int:user_id>/', delete_user, name='deleteuser'), # 사용자 정보 삭제 URL
    path('csrftoken/', csrf_token_view, name='csrf_token_view'), # csrftoken 가져오는 URL
    path('storeregis/', store_regis, name='store_regis'), # 가게 등록 URL
    path('mystoreinfo/<int:user_id>/', my_store_view, name='my_store_view'), # 내 가게 정보 조회 URL
    path('editstore/<int:store_id>/', update_store, name='update_store'), # 가게 정보 업데이트
    path('deletestore/<int:store_id>/', delete_store, name='delete_store'), # 가게 삭제
    path('newmenu/<int:store_id>/', create_menu, name='create_menu'), # 메뉴 등록
    path('getmenus/<int:store_id>/', store_menu_view, name='store_menu_view'), # 메뉴 가져오기
    path('deletemenu/<int:menu_id>/', delete_menu, name='delete_menu'), # 메뉴 삭제
    path('updatemenu/<int:menu_id>/', update_menu, name='update_menu'), # 메뉴 수정
    path('getallstores/', get_all_stores, name='get_all_stores'), # 모든 가게 정보 조회
    path('addorder/', add_new_order, name='add_new_order'), # 새로운 주문 추가
    path('getorderlist/<int:user_id>/', get_order_list, name='get_order_list'), # 주문 내역 조회
    path('cancelorder/<int:order_id>/', cancel_order, name='cancel_order'), # 주문 취소
    path('generateorders/', create_order_data, name="generate_orders"), # 주문 데이터 생성 url
    path('popular_menu/', get_popular_menu, name="popular_menu"),  # 주문량 많은 데이터 가져오기
    path('getneworder/<int:store_id>/', get_new_order, name='get_new_order'), # 새로운 주문 가게 주인에게 보여주기
    path('acceptorder/<int:order_id>/', accept_order, name='accept_order'), # 주문 수락
    path('rejectorder/<int:order_id>/', reject_order, name='reject_order'), # 주문 거절
    path('orderlength/<int:store_id>/', get_order_length, name='get_order_length'), # 새로 들어온 주문 갯수 받아오기
    path('riderinfo/', get_rider_info, name='get_rider_info'), # 배달원 정보 가져오기
    path('pickupfood/<int:order_id>/', delivering_order, name='delivering_order'), # 음식 픽업 후 배달중
    path('completedelivery/<int:order_id>/', completed_delivery, name='completed_delivery'), # 배달 완료
    path('newreview/<int:store_id>/', register_review, name='register_review'), # 새로운 리뷰 등록
    path('allreviews/<int:store_id>/', get_all_reviews, name='get_all_reviews'), # 가게의 모든 리뷰 가져오기
    path('removereview/<int:review_id>/', remove_reviews, name='remove_reviews'), # 특정 리뷰 삭제하기
    path('getmyreview/', get_my_review, name='get_my_review'), # 내가 작성한 리뷰 불러오기
    path('editmyreview/<int:review_id>/', edit_my_review, name='edit_my_review'), # 내가 작성한 리뷰 수정하기
    path('changelike/<int:user_id>/', toggle_like, name='toggle_like'), # 가게 찜하기
    path('getstorelikes/<int:user_id>/', get_store_likes, name='get_store_likes'), # 사용자가 찜한 가게 가져오기
    path('getcoupon/<int:user_id>/', get_store_coupon, name='get_store_coupon'), # 쿠폰 발급받기
    path('getallcoupons/<int:user_id>/', get_all_coupons, name='get_all_coupons'), # 사용자가 발급받은 모든 쿠폰들 가져오기
    path('getalluserreviews/<int:user_id>/', get_all_user_reviews, name='get_all_user_reviews'), # 사용자가 작성한 모든 리뷰 가져오기
    path('getlikedallstores/', get_all_liked_stores, name='get_all_liked_stores'), # 찜된 모든 가게 정보 가져오기
    path('getallmenus/<str:keyword>/', get_all_menus, name='get_all_menus'), # 검색 키워드를 포함하고 있는 메뉴의 가게 정보 반환
    path('getorderdetail/<int:orderid>/', get_order_detail, name='get_order_detail'), # 해당 주문 번호에 대한 모든 정보 가져오기
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)