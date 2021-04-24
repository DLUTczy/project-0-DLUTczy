import json
import uuid
import time

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from pymysql import IntegrityError

from Trade import settings
from tradeweb.models import *


def index(request):
    return render(request, "tradeweb/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tradeweb/login.html", {
                "message": "手机号或密码不正确."
            })
    else:
        return render(request, "tradeweb/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        phoneID = request.POST["phoneID"]
        if len(phoneID) != 11:
            return render(request, "tradeweb/register.html", {
                "message": "请输入合法长度的手机号."
            })
        # email = request.POST["email"]
        username = str(phoneID)
        phoneID = int(phoneID)
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tradeweb/register.html", {
                "message": "密码不匹配"
            })

        # Attempt to create new user
        if User.objects.filter(phoneID=phoneID):
            return render(request, "tradeweb/register.html", {
                "message": "手机号已被注册过！"
            })
        try:
            user = User.objects.create_user(phoneID=phoneID, username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "tradeweb/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tradeweb/register.html")


def student(request):
    if request.method == "GET":
        cities = tb_School.objects.all().distinct().order_by("area_id").values("area_id", "area_name")
        return render(request, "tradeweb/student.html", {
            "cities": cities,
        })
    elif request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        stuID = request.POST["student_id"]
        school_id = request.POST["school_id"]
        school = tb_School.objects.get(school_id=school_id)
        try:
            student = Student.objects.create(name=name, studentID=stuID, school=school)
            student.save()
            user = User.objects.get(username=username)
            user.student = student
            user.save()
        except IntegrityError:
            return render(request, "tradeweb/student.html", {
                "message": "学号已经认证."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def ajax_school(request):
    area_id = request.GET["area_id"]
    schools = tb_School.objects.filter(area_id=area_id).values("school_id", "school_name")
    list = []
    for school in schools:
        list.append(school)
    return JsonResponse(json.dumps(list), safe=False)


def release(request, phoneID):
    if request.method == "GET":
        phoneID = int(phoneID)
        goods = Goods.objects.filter(userID_id=phoneID)
        return render(request, "tradeweb/release.html",{
            "goods": goods,
        })
    elif request.method == "POST":
        goodName = request.POST["goodName"]
        userID = request.POST["userID"]
        user = User.objects.get(phoneID=userID)
        description = request.POST["description"]
        price = request.POST["price"]
        imageList = request.FILES.getlist("images")
        category = request.POST["category"]
        cate_list = str(category).split(" ")

        count = 0
        goodID = (int)(time.time() * 1000000)

        for image in imageList:
            if count == 0:
                Goods.objects.create(goodID=goodID, goodName=goodName, userID=user, goodImg=image, description=description,
                                         price=price, state="在售").save()
                print("保存成功")
            else:
                good = Goods.objects.get(goodID=goodID)
                Detail_Images.objects.create(goodID=good, img=image, priority=(count - 1)).save()
            with open(settings.MEDIA_ROOT + image.name, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                f.close()
            count += 1
        good = Goods.objects.get(goodID=goodID)
        for cate in cate_list:
            Category.objects.create(goodID=good, category=cate).save()
        request.method = "GET"
        return HttpResponseRedirect(reverse('release', args=[str(phoneID)]))


