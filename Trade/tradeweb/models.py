from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    phoneID = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=20)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, blank=True, null= True)


class Student(models.Model):
    studentID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    school = models.ForeignKey("tb_School", on_delete=models.CASCADE)


class tb_School(models.Model):
    school_id = models.IntegerField(primary_key=True)
    school_name = models.CharField(max_length=64)
    school_type = models.IntegerField()
    area_id = models.CharField(max_length=8)
    area_name = models.CharField(max_length=10)
    display_order = models.IntegerField()
