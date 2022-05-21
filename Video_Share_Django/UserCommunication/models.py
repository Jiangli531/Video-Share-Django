from django.db import models
from Weblogin.models import UserInfo
# Create your models here.


class VideoPartition(models.Model):
    videoPartName = models.CharField(max_length=30, null=False)
    videoPartID = models.AutoField(primary_key=True, null=False)


class UserLetter(models.Model):
    letterUser = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    letteredUser = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    letterText = models.TextField(null=False)
    letterTime = models.DateTimeField(auto_now_add=True, null=False)
    letterID = models.AutoField(primary_key=True, null=False)


class UserConnection(models.Model):
    # 用户关注表
    followerUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE) # 关注者
    followedUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE) # 被关注者
    connectID = models.AutoField(primary_key=True, null=False)


