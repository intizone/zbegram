import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)

    def __str__(self):
        return self.username
    

class UserReletion(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='to')

    def __str__(self):
        return f"{self.from_user.username} - {self.to_user.username}"


class Chat(models.Model):
    users = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        if len(self.users) > 2:
            raise AssertionError('Bu shaxsiy')
        super(Chat, self).save(*args, **kwargs)
    
    @property
    def last_message(self):
        message = Message.objects.filter(chat = self).last()
        return message
    
    @property
    def unread_messages(self):
        quantity = Message.objects.filter(
            chat = self,
            is_read = False
            ).count()
        return quantity




class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    body = models.TextField()
    file = models.FileField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.chat.id}-> {self.author.id}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class PostFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post/')

    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, str(self.file))
        if os.path.isfile(file_path):
            os.remove(file_path)
        super(PostFiles, self).delete(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField()

