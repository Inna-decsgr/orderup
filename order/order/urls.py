from django.contrib import admin
from django.urls import path, include  # include import
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 URL
    path('order/', include('orders.urls')),  # order 앱의 urls.py 포함
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)