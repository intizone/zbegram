from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserAPIView.as_view(), name='user-detail'),
    path('user-relation/', views.UserRelationAPIView.as_view(), name='user-relation-list'),
    path('user-relation/<int:pk>/', views.UserRelationAPIView.as_view(), name='user-relation-detail'),
    path('chat/', views.ChatAPIView.as_view(), name='chat-list'),
    path('chat/<int:pk>/', views.ChatAPIView.as_view(), name='chat-detail'),
    path('massage/', views.MassageAPIView.as_view(), name='massage-list'),
    path('massage/<int:pk>/', views.MassageAPIView.as_view(), name='massage-detail'),
    path('following/<int:pk>/', views.following, name='following'),
    path('follower/<int:pk>/', views.follower, name='follower'),
    
]