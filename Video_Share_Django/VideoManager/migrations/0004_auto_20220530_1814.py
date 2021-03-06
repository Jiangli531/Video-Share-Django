# Generated by Django 3.2 on 2022-05-30 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Weblogin', '0003_userinfo_useravatar'),
        ('VideoManager', '0003_alter_videoinfo_videopart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditrecord',
            name='adminUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Weblogin.userinfo'),
        ),
        migrations.AlterField(
            model_name='auditrecord',
            name='auditTime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
