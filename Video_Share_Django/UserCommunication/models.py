from django.db import models

# Create your models here.


class VideoPartition(models.Model):
    videoPartName = models.CharField(max_length=30, null=False)
    videoPartID = models.AutoField(primary_key=True, null=False)
