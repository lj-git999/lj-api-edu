from django.urls import path
from rest_framework_jwt import views as view

from user import views

urlpatterns = [
    path('login/', view.obtain_jwt_token),
    path('captcha/', views.CaptchaAPIView.as_view()),
    path('register/', views.UserAPIView.as_view()),
    path('message/', views.MessageAPIView.as_view()),
    path('phone/', views.PhoneAPIView.as_view()),
    path('login_phone/', views.LoginAPIView.as_view()),
    path('verify_phone/', views.PhoneVerifyAPIView.as_view()),

]
