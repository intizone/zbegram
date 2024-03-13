from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='User')
router.register(r'user-relations', views.UserRelationViewSet, basename='UserRelation')
router.register(r'chats', views.ChatViewSet, basename='Chat')
router.register(r'messages', views.MessageViewSet, basename='Message')

# router.register(r'posts', views.PostViewSet, basename='Post')
# router.register(r'post-files', views.PostFilesViewSet, basename='PostFiles')
# router.register(r'comments', views.CommentViewSet, basename='Comment')
# router.register(r'likes', views.LikeViewSet, basename='Like')
# router.register(r'auth', views.AuthViewSet, basename='Auth')


urlpatterns = [
    path('router/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    
    path('users/', views.user_viewset, name='user-list'),
    path('users/<int:pk>/', views.user_detail_viewset, name='user-detail'),
    path('user-relations/', views.user_relation_viewset, name='user-relation-list'),
    path('chats/', views.chat_viewset, name='chat-list'),
    path('chats/<int:pk>/', views.chat_detail_viewset, name='chat-detail'),
    path('messages/', views.message_viewset, name='message-list'),
    path('messages/<int:pk>/', views.message_detail_viewset, name='message-detail'),
    # path('', views.list_data)
]