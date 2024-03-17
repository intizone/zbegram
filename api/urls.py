from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserAPIView.as_view(), name='user-list'),
    path('user/<str:code>/', views.UserAPIView.as_view(), name='user-detail'),
    path('user-posts/<str:code>/', views.user_posts),
    path('user-search/<str:q>/', views.search, name='user-search'),

    path('user-relation/', views.UserRelationAPIView.as_view(), name='user-relation-list'),
    path('user-relation/<int:pk>/', views.UserRelationAPIView.as_view(), name='user-relation-detail'),

    path('chat-filter/<str:code>/', views.chat_filter, name='chat-filter'),
    path('chat/', views.ChatAPIView.as_view(), name='chat-list'),
    path('chat/<str:code>/', views.ChatAPIView.as_view(), name='chat-detail'),

    path('massage/', views.MassageAPIView.as_view(), name='massage-list'),
    path('massage/<str:code>/', views.MassageAPIView.as_view(), name='massage-detail'),

    path('following/<str:code>/', views.following, name='following'),
    path('follower/<str:code>/', views.follower, name='follower'),
    path('following-posts/', views.following_posts),

    path('comment/', views.CommentAPIView.as_view(), name='comment-list'),
    path('comment/<int:pk>/', views.CommentAPIView.as_view(), name='comment-detail'),

    path('post-detail/<str:code>/', views.post_detail),
    path('post/', views.PostAPIView.as_view(), name='post-list'),
    path('post/<str:code>/', views.PostAPIView.as_view(), name='post-detail'),
    ]