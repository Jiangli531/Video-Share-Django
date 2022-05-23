from django.db import models

import UserCommunication
from UserCommunication.models import VideoPartition
from Weblogin.models import UserInfo

# Create your models here.
def video_cover_directory_path(instance, filename):
    # 文件上传到 MEDIA_ROOT/videoCover/video_<id>/<filename>目录中
    return 'videoCover/video_{0}/{1}'.format(instance.videoID, filename)


class VideoInfo(models.Model):
    videoID = models.AutoField(primary_key=True)
    videoName = models.CharField(max_length=40)
    videoInformation = models.CharField(max_length=500, blank=True)
    videoPath = models.CharField(max_length=200)
    videoCoverPath = models.ImageField(upload_to=video_cover_directory_path, blank=True)
    videoPlayNum = models.IntegerField(default=0)
    videoLikeNum = models.IntegerField(default=0)
    videoFavorNum = models.IntegerField(default=0)
    videoPart = models.OneToOneField(VideoPartition, on_delete=models.CASCADE)
    videoUpUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    videoUpTime = models.DateTimeField(auto_now_add=True)
    videoUpState = models.BooleanField(default=False)

    class Meta:
        db_table = 'videos'
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class AuditRecord(models.Model):
    # 审核记录
    auditVideo = models.ForeignKey(VideoInfo, on_delete=models.CASCADE)
    complainUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='complain_user') # 投诉的用户
    complainedUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='complained_user') # 被投诉的用户
    adminUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE) # 审核人
    auditTime = models.DateTimeField(auto_now_add=True) # 审核时间
    auditResult = models.BooleanField(default=False) # 审核结果
    auditID = models.AutoField(primary_key=True) # 审核记录ID
    complainReason = models.CharField(max_length=400) # 投诉理由

    class Meta:
        db_table = 'AuditRecord'
        verbose_name = '审核记录'
        verbose_name_plural = verbose_name
        ordering = ['-auditTime']
