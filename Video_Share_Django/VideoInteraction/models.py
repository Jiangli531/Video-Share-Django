from django.db import models
from Weblogin.models import UserInfo
from VideoManager.models import VideoInfo

# Create your models here.


class Favourites(models.Model):
    favorUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    favorVideo = models.ForeignKey(VideoInfo, on_delete=models.CASCADE)
    favorTime = models.DateTimeField(auto_now_add=True)     # 自动添加时间
    favorID = models.AutoField(primary_key=True)    # 自增长主键

    class Meta:
        db_table = 'Favourites'
        verbose_name = '收藏夹'
        verbose_name_plural = verbose_name
        ordering = ['-favorTime']


class LikeRecord(models.Model):
    likeID = models.AutoField(primary_key=True)
    likeUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE) # 点赞用户
    likeVideo = models.ForeignKey(VideoInfo, on_delete=models.CASCADE)
    likedUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE) # 被点赞用户
    likeTime = models.DateTimeField(auto_now_add=True)     # 自动添加时间

    class Meta:
        db_table = 'LikeRecord'
        verbose_name = '点赞记录'
        verbose_name_plural = verbose_name
        ordering = ['-likeTime']


class VideoComment(models.Model):
    commentID = models.AutoField(primary_key=True)
    commentUpUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)  # 被评论用户
    commentComUser = models.ForeignKey(UserInfo, on_delete=models.CASCADE)  # 评论用户
    commentVideo = models.ForeignKey(VideoInfo, on_delete=models.CASCADE)
    commentContent = models.TextField(max_length=500)
    commentTime = models.DateTimeField(auto_now_add=True)
    parentComment = models.ForeignKey('self', on_delete=models.CASCADE, null=True) # 父评论

    class Meta:
        db_table = 'VideoComment'
        verbose_name = 'VideoComment'
        verbose_name_plural = verbose_name
        ordering = ['-commentTime']
