from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.UserReletion)
admin.site.register(models.Chat)
admin.site.register(models.Message)
admin.site.register(models.Post)
admin.site.register(models.PostFiles)
admin.site.register(models.Comment)
admin.site.register(models.Like)