from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class User(AbstractUser):
    phoneID = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=20)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, blank=True, null=True)
    REQUIRED_FIELDS = ['email', 'phoneID','nickname', 'password']


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
    price = models.DecimalField(max_digits=20, decimal_places=2)
    state = models.CharField(max_length=10)  # 在售 被拍下 已售
    number = models.IntegerField()


@receiver(pre_delete, sender=Goods)
def goodImg_delete(sender, instance, **kwargs):
    instance.goodImg.delete(False)


class Detail_Images(models.Model):
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)
    img = models.ImageField(upload_to="img")
    priority = models.IntegerField()


@receiver(pre_delete, sender=Detail_Images)
def detailImg_delete(sender, instance, **kwargs):
    instance.img.delete(False)


class Messages(models.Model):
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
    fromID = models.CharField(max_length=20)
    seq = models.IntegerField(default=0)
    type = models.CharField(max_length=10)
    contentID = models.IntegerField(default=0)
    msgTime = models.DateTimeField(auto_now_add=True)
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)


class Content_text(models.Model):
    CID = models.AutoField(primary_key=True)
    Cstr = models.CharField(max_length=200)


class Content_Image(models.Model):
    CID = models.AutoField(primary_key=True)
    CImage = models.ImageField(upload_to="img")


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
    beforeOrder = models.ForeignKey("BeforeOrder", on_delete=models.CASCADE)
    got = models.IntegerField()  # 收到商品为 1 未收到 0


class Category(models.Model):
    goodID = models.ForeignKey("Goods", on_delete=models.CASCADE)
    category = models.CharField(max_length=20)


class BeforeOrder(models.Model):
    orderID = models.BigIntegerField(primary_key=True)
    orderTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)  # 0 代表未支付 1 代表支付
    userID = models.ForeignKey("User", on_delete=models.CASCADE)
