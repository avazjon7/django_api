from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user import views

urlpatterns = [
    path('register/', views.UserRegisterApiView.as_view(), name='register-user'),
    path('login/', TokenObtainPairView.as_view(), name='login-user'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
