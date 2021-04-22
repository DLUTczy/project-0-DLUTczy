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


class Goods(models.Model):
    goodID = models.BigIntegerField(primary_key=True)
    goodName = models.CharField(max_length=100)
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    goodImg = models.ImageField(upload_to="img")
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_length=20,max_digits=2)
    state = models.CharField(max_length=10)


class  Detail_Images(models.Model):
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)
    img = models.ImageField(upload_to="img")
    priority = models.IntegerField()


class Messages(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    fromID = models.CharField(max_length=20)
    seq = models.IntegerField(default=0)
    type = models.CharField(max_length=10)
    contentID = models.IntegerField(default=0)

class Content_text(models.Model):
    CID = models.AutoField(primary_key=True)
    Cstr = models.CharField(max_length=200)


class Content_Image(models.Model):
    CID = models.AutoField(primary_key=True)
    CImage=models.ImageField(upload_to="img")


class Comments(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    comTime = models.DateTimeField(auto_now_add=True)


class Wants(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)


class Address(models.Model):
    addressID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)


class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)
    orderTime = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=100)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)
