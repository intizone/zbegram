from rest_framework.serializers import ModelSerializer

from main import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'last_login']
        

class UserRealtionSerializer(ModelSerializer):
    class Meta:
        model = models.UserReletion
        fields = '__all__'


class FollowingSerializer(ModelSerializer):
    class Meta:
        model = models.UserReletion
        fields = ['from_user',]
        depth=1


class FollowerSerializer(ModelSerializer):
    class Meta:
        model = models.UserReletion
        fields = ['to_user',]
        depth=1
        

class ChatSerializer(ModelSerializer):
    class Meta:
        model = models.Chat
        fields = ['id', 'username']
        
        
class MassageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'

class ChatListSerializer(ModelSerializer):
    last_message = MassageSerializer(read_only=True)
    class Meta:
        model = models.Chat
        fields = ['id', 'last_message', 'unread_messages', 'users']

class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['author', 'title', 'body']

class PostFilesSerializer(ModelSerializer):
    class Meta:
        model = models.PostFiles
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['author', 'post', 'text', 'reply']

class LikeSerializer(ModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'