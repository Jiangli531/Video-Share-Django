from django.db import models

# Create your models here.


class VideoPartition(models.Model):
    VideoPartName = models.CharField(max_length=30)
    VideoPartID = models.AutoField(primary_key=True)
