"""spm_pj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from main import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('stu_index/<str:stu_id>/', views.stu_index, name='stu_index'),
    path('stu_room/<str:stu_id>/<str:building_id>/', views.stu_room, name='stu_room'),
    path('stu_seat/<str:stu_id>/<str:room_id>/', views.stu_seat, name='stu_seat'),
    path('stu_record/<str:stu_id>/', views.stu_record, name='stu_record'),
    path('test', views.test, name='test'),
    path('qrcode/<str:seat_id>', views.qrcode, name='qrcode'),
    path('signin', views.signin, name='signin'),
    # path('mng_index/<str:manager_id>/', views.mng_index, name='mng_index'),
    # path('mng_index/<str:manager_id>/<str:building_id>/', views.mng_building, name='mng_building'),
    # path('mng_index/<str:manager_id>/<str:room_id>/', views.mng_room, name='mng_room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

