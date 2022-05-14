from django.db import models

# Create your models here.
def user_portrait_directory_path(instance, filename):
    # 文件上传到 MEDIA_ROOT/portrait/user_<id>/<filename>目录中
    return 'portrait/user_{0}/{1}'.format(instance.id, filename)


class Userinfo(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)
    userpassword = models.CharField(max_length=128)
    useremail = models.EmailField(unique=True)
    userInformation = models.CharField(max_length=500, blank=True)
    userPortrait = models.ImageField(upload_to=user_portrait_directory_path(), blank=True)
    userLimit = models.BooleanField(default=False)
    userSex = models.CharField(max_length=32, choices=gender, default="男")
    userBirthday = models.DateField()


    def __str__(self):
        return self.username
