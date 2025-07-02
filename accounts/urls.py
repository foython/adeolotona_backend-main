from django.urls import path
from . import views

urlpatterns = [
    path('normal_register/', views.normal_register, name='normal_register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path("normal_login/", views.normal_login, name='normal_login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('change_password/', views.change_password, name='change_password'),
    path('social_login_register/', views.social_login_register, name='social_login_register')
]
