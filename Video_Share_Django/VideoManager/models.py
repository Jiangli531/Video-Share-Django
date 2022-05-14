from django.db import models
from UserCommunication.models import VideoPartition
# Create your models here.
def video_cover_directory_path(instance, filename):
    # 文件上传到 MEDIA_ROOT/portrait/video_<id>/<filename>目录中
    return 'videoCover/video_{0}/{1}'.format(instance.videoID, filename)


class VideoInfo(models.Model):
    videoID = models.AutoField(primary_key=True)
    videoName = models.CharField(max_length=40)
    videoInformation = models.CharField(max_length=500, blank=True)
    videoPath = models.CharField(max_length=200)
    videoCoverPath = models.ImageField(upload_to=video_cover_directory_path(), blank=True)
    videoPlayNum = models.IntegerField(default=0)
    videoFavorNum = models.IntegerField(default=0)
    videoPart = models.OneToOneField(VideoPartition, on_delete=models.CASCADE)
    videoUpUser = models.ForeignKey('UserCommunication.UserInfo', on_delete=models.CASCADE)
    videoUpTime = models.DateTimeField(auto_now_add=True)
    videoUpState = models.BooleanField(default=False)