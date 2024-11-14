from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import login_view, signup_view, update_user, get_user, delete_user, csrf_token_view, store_regis, my_store_view, update_store, delete_store, create_menu, store_menu_view, delete_menu, update_menu, get_all_stores, add_new_order, get_order_list

urlpatterns = [
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
    path('getorderlist/<int:user_id>/', get_order_list, name='get_order_list'), # 메뉴 삭제
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)