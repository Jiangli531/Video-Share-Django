# Generated by Django 4.0.3 on 2022-06-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoManager', '0006_merge_20220601_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditrecord',
            name='isAudit',
            field=models.BooleanField(default=False),
        ),
    ]
