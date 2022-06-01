from django.db import models

# Create your models here.


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=20)
    age = models.IntegerField()
    phone = models.CharField(max_length=11)
    city = models.CharField(max_length=20)


class Power(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=20)


class Role(models.Model):
    rid = models.AutoField(primary_key=True)
    rname = models.CharField(max_length=20)


class RP(models.Model):
    id = models.AutoField(primary_key=True)
    rid = models.ForeignKey(Role, on_delete=models.CASCADE)
    pid = models.ForeignKey(Power, on_delete=models.CASCADE)


class UR(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    rid = models.ForeignKey(Role, on_delete=models.CASCADE)
