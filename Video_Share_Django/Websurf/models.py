from django.db import models

# Create your models here.
from UserCommunication.models import VideoPartition
from VideoManager.models import VideoInfo
from Weblogin.models import UserInfo


class BrowseRecord(models.Model):
    browseVideo = models.ForeignKey(VideoInfo, on_delete=models.CASCADE)
    browseUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    browseTime = models.DateTimeField(auto_now_add=True)
    browseDuration = models.IntegerField(default=0) #单位秒
    # browseVideoPartition = models.ForeignKey(VideoPartition, on_delete=models.CASCADE)
    browseVideoPartition = models.CharField(max_length=128)
    browseID = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'BrowseRecord'
        verbose_name = '浏览记录表'
        verbose_name_plural = verbose_name
        ordering = ['-browseTime']
