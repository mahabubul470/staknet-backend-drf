from django.urls import path
from core.views import UserApiView, AuthApiView, ProfileApiView

urlpatterns = [
    path('user/', UserApiView.as_view(), name='user-registration'),
    path('login/', AuthApiView.as_view(), name='user-login'),
    path('profile/', ProfileApiView.as_view(), name='user-profile'),
]
