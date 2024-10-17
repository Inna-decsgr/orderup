from django.contrib import admin
from django.urls import path, include  # include import

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 URL
    path('order/', include('orders.urls')),  # order 앱의 urls.py 포함
]
