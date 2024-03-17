from rest_framework.serializers import ModelSerializer
from main import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['code', 'username', 'email', 'first_name', 'last_name', 'avatar', 'last_login']
        

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
        fields = ['code', 'username']
        
        
class MassageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'

class ChatListSerializer(ModelSerializer):
    last_message = MassageSerializer(read_only=True)
    class Meta:
        model = models.Chat
        fields = ['code', 'last_message', 'unread_messages', 'users']

class FileSerializer(ModelSerializer):
    class Meta:
        model = models.PostFiles
        fields = ['file',]

class PostSerializer(ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    class Meta:
        model = models.Post
        fields = ['code', 'title', 'author', 'body' , 'date', 'like', 'dislike', 'files']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'

class LikeSerializer(ModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'