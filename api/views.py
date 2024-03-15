from django.db.models import Q
from main import models
from . import serializers

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status   



class UserAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        # way 1
        users = models.User.objects.all()
        if q:
            users.filter(
                Q(username__icontains=q)| 
                Q(first_name__iconatins=q)| 
                Q(last_name__iconatins=q)|
                Q(email__icontains=q)
                )
        # way 2
        # if q:
        #     users = models.User.objects.filter(
        #         Q(username__icontains=q)| 
        #         Q(first_name__iconatins=q)| 
        #         Q(last_name__iconatins=q)|
        #         Q(email__icontains=q)
        #     )
        # else:
        #     users = models.User.objects.all()

        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            user = request.user
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class UserRelationAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        following = models.UserReletion.objects.filter(from_user=user)
        follower = models.UserReletion.objects.filter(to_user=user)
        following_ser = serializers.FollowingSerializer(following, many=True)
        follower_ser = serializers.FollowerSerializer(follower, many=True)
        data = {
            'following':following_ser.data,
            'follower':follower_ser.data,
        }
        return Response(data)


    def post(self, request, *args, **kwargs):
        try:
            from_user = request.user
            to_user = request.data['to_user']
            models.UserReletion.objects.create(from_user=from_user, to_user=to_user)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            to_user = models.User.objects.get(pk=pk)
            reletion = models.UserReletion.objects.get(
                from_user=request.user,
                to_user = to_user
                )
            reletion.delete()
            return Response(status=status.HTTP_200_OK)
        except models.UserReletion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
class ChatAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        user = request.user
        chats = models.Chat.objects.filter(users=user)
        chats_ser = serializers.ChatListSerializer(chats)
        return Response(chats_ser.data)
        # try:
        #     instance = models.Chat.objects.get(pk=pk)
        # except models.Chat.DoesNotExist:
        #     return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

        # serializer = serializers.ChatSerializer(instance)
        # return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        try:
            chat = models.Chat.objects.get(pk=pk)
        except models.Chat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class MassageAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.MassageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            massage = models.Message.objects.get(pk=pk)
            assert massage.author == request.user
        except models.Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MassageSerializer(massage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            massage = models.Message.objects.get(pk=pk)
            assert massage.author == request.user
        except models.Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        massage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view
def following(request, pk):
    user = models.User.objects.get(pk=pk)
    user_reletion = models.UserReletion.objects.filter(from_user=user)
    serializer_data = serializers.FollowingSerializer(user_reletion, many=True)
    return serializer_data.data

@api_view
def follower(request, pk):
    user = models.User.objects.get(pk=pk)
    user_reletion = models.UserReletion.objects.filter(to_user=user)
    serializer_data = serializers.FollowerSerializer(user_reletion, many=True)
    return serializer_data.data


class PostAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk:
            try:
                instance = models.Post.objects.get(pk=pk)
            except models.Post.DoesNotExist:
                return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.PostSerializer(instance)
            return Response(serializer.data)
        else:
            posts = models.Post.objects.all()
            serializer = serializers.PostSerializer(posts, many=True)
            return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        try:
            post = models.Post.objects.get(pk=pk)
            assert post.author == request.user
        except models.Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            post = models.Post.objects.get(pk=pk)
            assert post.author == request.user
        except models.Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view
def post_filter(request, pk):
    posts = models.Post.objects.filter(author=pk)
    serializer = serializers.PostSerializer(posts, many=True)
    return serializer.data

class LikeAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            like = models.Like.objects.get(pk=pk)
            assert like.author == request.user
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk=None, format=None):
        if pk:
            try:
                instance = models.Like.objects.get(pk=pk)
            except models.Like.DoesNotExist:
                return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.LikeSerializer(instance)
            return Response(serializer.data)
        else:
            likes = models.Like.objects.all()
            serializer = serializers.LikeSerializer(likes, many=True)
            return Response(serializer.data)
        
    def put(self, request, pk, *args, **kwargs):
        try:
            like = models.Like.objects.get(pk=pk)
            assert like.author == request.user
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.LikeSerializer(like, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view
def like_filter(request, pk):
    likes = models.Like.objects.filter(post=pk)
    serializer = serializers.LikeSerializer(likes, many=True)
    return serializer.data

class CommentAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk:
            try:
                instance = models.Comment.objects.get(pk=pk)
            except models.Comment.DoesNotExist:
                return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = serializers.CommentSerializer(instance)
            return Response(serializer.data)
        else:
            comments = models.Comment.objects.all()
            serializer = serializers.CommentSerializer(comments, many=True)
            return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        try:
            comment = models.Comment.objects.get(pk=pk)
            assert comment.author == request.user
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            comment = models.Comment.objects.get(pk=pk)
            assert comment.author == request.user
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)