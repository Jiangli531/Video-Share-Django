from django.db import models
from Weblogin.models import UserInfo
# Create your models here.


class VideoPartition(models.Model):
    videoPartName = models.CharField(max_length=30, null=False)
    videoPartID = models.AutoField(primary_key=True, null=False)

    class Meta:
        db_table = 'VideoPartition'
        verbose_name = '视频分区'
        verbose_name_plural = verbose_name


class UserLetter(models.Model):
    letterUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='ler_user')
    letteredUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='led_user')
    letterText = models.TextField(null=False)
    letterTime = models.DateTimeField(auto_now_add=True, null=False)
    letterID = models.AutoField(primary_key=True, null=False)

    class Meta:
        db_table = 'UserLetter'
        verbose_name = '用户私信'
        verbose_name_plural = verbose_name
        ordering = ['-letterTime']


class UserConnection(models.Model):
    # 用户关注表
    followerUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='fer_user') # 关注者
    followedUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='fed_user') # 被关注者
    connectID = models.AutoField(primary_key=True, null=False)

    class Meta:
        db_table = 'UserConnection'
        verbose_name = '用户关注表'
        verbose_name_plural = verbose_name

