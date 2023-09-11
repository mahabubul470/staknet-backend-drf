import core.views as views
from django.urls import path

urlpatterns = [
    path('users/', views.UserApiView.as_view(), name='users'),
    path('login/', views.AuthApiView.as_view(), name='user-login'),
    path('profile/', views.ProfileApiView.as_view(), name='user-profile'),
    path('posts/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<str:post_id>/like/',
         views.PostLikeView.as_view(), name='post-like'),
    path('posts/<str:post_id>/comment/',
         views.PostCommentView.as_view(), name='post-comment'),
    path('connections/', views.ConnectionView.as_view(), name='connection'),
]
