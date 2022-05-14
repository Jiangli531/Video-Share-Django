from django.db import models

# Create your models here.
import Weblogin.models


class VideoPartition(models.Model):
    videoPartName = models.CharField(max_length=30, null=False)
    videoPartID = models.AutoField(primary_key=True, null=False)


class UserLetter(models.Model):
    letterUser = models.OneToOneField('Userinfo', on_delete=models.CASCADE)
    letteredUser = models.OneToOneField('Userinfo', on_delete=models.CASCADE)
    letterText = models.TextField(null=False)
    letterTime = models.DateTimeField(null=False)
    letterID = models.AutoField(primary_key=True, null=False)