from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserAPIView.as_view()),
    path('user-relation/', views.UserRelationAPIView.as_view()),
    path('chat/', views.UserAPIView.as_view()),
    path('massage/', views.UserAPIView.as_view()),
    path('following/<int:pk>/', views.following),
    path('follower/<int:pk>/', views.follower),
    path('following-posts/', views.following_posts),
    path('user-posts/<int:pk>/', views.user_posts),
    path('post-detail/<int:pk>/', views.post_detail),
]