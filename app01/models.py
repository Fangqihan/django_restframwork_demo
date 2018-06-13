from django.db import models

class Groups(models.Model):
    title = models.CharField(max_length=32)


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    type = models.IntegerField(choices=((1,'普通用户'),(2, '管理用户')), default=1)
    email = models.EmailField(max_length=64)
    user_group = models.ForeignKey(Groups, default=1)


class Token(models.Model):
    value = models.CharField(max_length=64)
    user = models.OneToOneField(UserInfo)

