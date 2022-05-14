from django.db import models

# Create your models here.
import Weblogin.models


class VideoPartition(models.Model):
    VideoPartName = models.CharField(max_length=30, null=False)
    VideoPartID = models.AutoField(primary_key=True, null=False)


class UserLetter(models.Model):
    letterUserID = models.OneToOneField('Userinfo', on_delete=models.CASCADE)
    letterUserName = models.CharField(max_length=30, null=False)
    letteredUserID = models.OneToOneField('Userinfo', on_delete=models.CASCADE)
    letteredUserName = models.CharField(max_length=30, null=False)
    letterText = models.TextField(null=False)
    letterTime = models.DateTimeField(null=False)
    letterID = models.AutoField(primary_key=True, null=False)