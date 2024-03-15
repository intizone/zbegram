from rest_framework.serializers import ModelSerializer
from main import models

class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class UserRelationSerializer(ModelSerializer):
    class Meta:
        model = models.UserRelation
        fields = '__all__'


class ChatSerializer(ModelSerializer):
    class Meta:
        model = models.Chat
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = '__all__'


class PostFilesSerializer(ModelSerializer):
    class Meta:
        model = models.PostFiles
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class LikeSerializer(ModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'