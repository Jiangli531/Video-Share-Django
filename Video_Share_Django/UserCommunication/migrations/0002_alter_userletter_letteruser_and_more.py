# Generated by Django 4.0.3 on 2022-06-01 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Weblogin', '0004_userinfo_totallikenum'),
        ('UserCommunication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userletter',
            name='letterUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ler_user', to='Weblogin.userinfo'),
        ),
        migrations.AlterField(
            model_name='userletter',
            name='letteredUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='led_user', to='Weblogin.userinfo'),
        ),
    ]
