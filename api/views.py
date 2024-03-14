from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from main import models
from . import serializers



class UserViewSet(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        queryset = models.User.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset


class UserRelationViewSet(ModelViewSet):
    queryset = models.UserRelation.objects.all()
    serializer_class = serializers.UserRelationSerializer



class ChatViewSet(ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        messages = models.Message.objects.filter(chat=instance)
        message_serializer = serializers.MessageSerializer(messages, many=True)

        data = serializer.data
        data['messages'] = message_serializer.data

        return Response(data, status=status.HTTP_200_OK)


class MessageViewSet(ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer

# class PostViewSet(ModelViewSet):
#     queryset = models.Post.objects.all()
#     serializer_class = serializers.PostSerializer

# class PostFilesViewSet(ModelViewSet):
#     queryset = models.PostFiles.objects.all()
#     serializer_class = serializers.PostFilesSerializer

# class CommentViewSet(ModelViewSet):
#     queryset = models.Comment.objects.all()
#     serializer_class = serializers.CommentSerializer

# class LikeViewSet(ModelViewSet):
#     queryset = models.Like.objects.all()
#     serializer_class = serializers.LikeSerializer

# class AuthViewSet(ModelViewSet):
#     queryset = models.User.objects.all()
#     serializer_class = serializers.UserSerializer

#     def get_queryset(self):
#         queryset = models.User.objects.all()
#         username = self.request.query_params.get('username', None)
#         password = self.request.query_params.get('password', None)
#         if username is not None and password is not None:
#             queryset = queryset.filter(username=username, password=password)
#         return queryset
    


user_viewset = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail_viewset = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_relation_viewset = UserRelationViewSet.as_view({
    'post': 'create',
    'delete': 'destroy'
})

chat_viewset = ChatViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

chat_detail_viewset = ChatViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

message_viewset = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

message_detail_viewset = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})