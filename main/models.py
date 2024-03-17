import string
import random

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, blank=True)


    def __str__(self):
        return self.username

class UserReletion(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='to')

    def __str__(self):
        return f"{self.from_user.username} - {self.to_user.username}"

class Chat(models.Model):
    users = models.ManyToManyField(User)
    code = models.CharField(max_length=10, unique=True, blank=True)

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

class ChatUser(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    body = models.TextField()
    file = models.FileField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    code = models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self):
        return f"{self.chat.id}-> {self.author.id}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, unique=True, blank=True)


    @property
    def like(self):
        return Like.objects.filter(post=self, status=True).count()

    @property
    def dislike(self):
        return Like.objects.filter(post=self, status=False).count()

class PostFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='post/')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment', on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, blank=True)

    
    def __str__(self):
        return f"{self.author.username} - {self.post.title}"

class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField()

def generate_unique_code():
    length = 10
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if User.objects.filter(code=code).count() == 0:
            break
    return code

@receiver(pre_save, sender=User)
@receiver(pre_save, sender=Chat)
@receiver(pre_save, sender=Message)
@receiver(pre_save, sender=Post)
@receiver(pre_save, sender=Comment)
def add_unique_code(sender, instance, **kwargs):
    if not instance.code:
        instance.code = generate_unique_code()

