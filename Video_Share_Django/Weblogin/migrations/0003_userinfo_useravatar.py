# Generated by Django 3.2 on 2022-05-30 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Weblogin', '0002_alter_userinfo_userbirthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='userAvatar',
            field=models.CharField(default='https://nohesitate-1312201606.cos.ap-beijing.myqcloud.com/UserAvatar/head.jpeg', max_length=500),
        ),
    ]