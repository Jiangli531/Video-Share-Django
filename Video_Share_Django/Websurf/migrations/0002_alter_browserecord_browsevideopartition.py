# Generated by Django 3.2 on 2022-05-29 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Websurf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browserecord',
            name='browseVideoPartition',
            field=models.CharField(max_length=128),
        ),
    ]