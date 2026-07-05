from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, MeView, ChangePasswordView, DeleteAccountView
urlpatterns=[path('register/',RegisterView.as_view()),path('login/',TokenObtainPairView.as_view()),path('refresh/',TokenRefreshView.as_view()),path('logout/',LogoutView.as_view()),path('me/',MeView.as_view()),path('change-password/',ChangePasswordView.as_view()),path('delete-account/',DeleteAccountView.as_view())]
