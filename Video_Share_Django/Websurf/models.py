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
    browseVideoPartition = models.ForeignKey(VideoPartition, on_delete=models.CASCADE)
    browseID = models.AutoField(primary_key=True)