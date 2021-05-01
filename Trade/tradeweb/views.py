import json
import uuid
import time

from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from pymysql import IntegrityError

from Trade import settings
from tradeweb.models import *


def index(request):
    user = getattr(request, 'user', None)
    if user.is_authenticated and user.student is not None:
        goods = Goods.objects.filter(userID__student__school_id=user.student.school_id).filter(state="在售")
    else:
        goods = Goods.objects.all().filter(state="在售")
    return render(request, "tradeweb/index.html", {
        "goods": goods,
    })


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


def shopping_car(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    phoneID = user.phoneID
    want_list = Wants.objects.filter(userID_id=phoneID).values("goodID_id").annotate(count=Count('goodID_id')).values(
        'goodID', "goodID__price", "goodID__goodImg", "goodID__state", "goodID__goodName", "goodID__number", 'count')
    return render(request, "tradeweb/wantspage.html", {
        "want_list": want_list,
    })


def release(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    phoneID = user.phoneID
    if request.method == "GET":
        goods = Goods.objects.filter(userID_id=phoneID, state="在售")
        return render(request, "tradeweb/release.html", {
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
                Goods.objects.create(goodID=goodID, goodName=goodName, userID=user, goodImg=image,
                                     description=description,
                                     price=price, state="在售", number=1).save()
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
        return HttpResponseRedirect(reverse('release'))


def details(request, goodID):
    user = getattr(request, 'user', None)
    good = Goods.objects.get(goodID=goodID)
    if user.is_authenticated and user.phoneID == good.userID_id:
        imgs = Detail_Images.objects.filter(goodID_id=goodID)
        comments = Comments.objects.filter(goodID_id=goodID)
        return render(request, "tradeweb/details.html", {
            "good": good,
            "imgs": imgs,
            "comments": comments,
        })

    imgs = Detail_Images.objects.filter(goodID_id=goodID)
    comments = Comments.objects.filter(goodID_id=goodID)
    return render(request, "tradeweb/details.html", {
        "good": good,
        "imgs": imgs,
        "comments": comments,
    })


@csrf_exempt
def ajax_comment(request):
    goodID = request.GET["goodID"]
    good = Goods.objects.get(goodID=goodID)
    userID = request.GET["userID"]
    phone = User.objects.get(phoneID=userID)
    content = request.GET["content"]
    Comments.objects.create(goodID=good, userID=phone, content=content).save()
    return JsonResponse(None, safe=False)


@csrf_exempt
def ajax_want(request):
    goodID = request.GET["goodID"]
    userID = request.GET["userID"]
    if len(Wants.objects.filter(goodID_id=goodID, userID_id=userID)) == 0:
        good = Goods.objects.get(goodID=goodID)
        phone = User.objects.get(phoneID=userID)
        Wants.objects.create(goodID=good, userID=phone).save()
    return JsonResponse(None, safe=False)


@csrf_exempt
def ajax_nick(request):
    nickname = request.GET["nickname"]
    phoneID = request.GET["userID"]
    user = User.objects.get(phoneID=phoneID)
    user.nickname = nickname
    user.save()
    return JsonResponse(None, safe=False)


@csrf_exempt
def ajax_mail(request):
    email = request.GET["mail"]
    phoneID = request.GET["userID"]
    user = User.objects.get(phoneID=phoneID)
    user.email = email
    user.save()
    return JsonResponse(None, safe=False)


def add_address(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    address = request.POST["address"]
    user = User.objects.get(phoneID=user.phoneID)
    Address.objects.create(userID=user, address=address).save()
    return HttpResponseRedirect(reverse("address"))


def infopage(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    return render(request, "tradeweb/myinfopage.html")


def address(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    phoneID = user.phoneID
    addresses = Address.objects.filter(userID_id=phoneID)
    return render(request, "tradeweb/address.html", {
        "addresses": addresses,
    })


@csrf_exempt
def ajax_deladdress(request):
    addressID = request.GET["addressID"]
    Address.objects.get(addressID=addressID).delete()
    return JsonResponse(None, safe=False)


def message(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    return render(request, "tradeweb/message.html")


def buyer(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    beforeOrder = BeforeOrder.objects.filter(userID_id=user.phoneID, status=1)
    orders = Order.objects.filter(beforeOrder__in=beforeOrder).order_by("-orderTime")
    return render(request, "tradeweb/buyertrade.html", {
        "orders": orders,
    })


def delwantgoods(request):
    goodID = request.POST["goodID"]
    phoneID = getattr(request, 'user', None).phoneID
    Wants.objects.filter(goodID=goodID, userID=phoneID).delete()
    return HttpResponseRedirect(reverse("shopping_car"))


def bebought(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    goods = Goods.objects.filter(userID_id=user.phoneID).filter(~Q(state="在售"))
    orders = Order.objects.filter(goodID__in=goods)

    return render(request, "tradeweb/bebought.html", {
        "orders": orders,
    })


def placeOrder(request):
    user = getattr(request, 'user', None)
    goodID_list = []
    data = request.POST
    for key, value in data.items():
        if key.startswith("check_"):
            goodID = key.split("_")[1]
            goodID_list.append(int(goodID))

    orderID = int(time.time() * 1000000)
    addresses = Address.objects.filter(userID_id=user.phoneID)
    if len(addresses) == 0:
        return HttpResponseRedirect(reverse('address'))

    address = addresses.first()
    beforeOrder = BeforeOrder()
    totle_money = 0
    if goodID_list:
        beforeOrder.orderID = orderID
        beforeOrder.userID = user
        beforeOrder.save()
    else:
        return HttpResponseRedirect(reverse("shopping_car"))
    for goodID in goodID_list:
        order = Order()
        order.beforeOrder_id = orderID
        good = Goods.objects.get(goodID=goodID)
        totle_money = totle_money+good.price
        good.state = "被拍下"
        good.save()
        order.goodID = good
        order.userID = user
        order.address = address
        order.remark = ""
        order.got = 3
        order.save()

    orders = Order.objects.filter(beforeOrder=beforeOrder)
    return render(request, "tradeweb/placeOrder.html", {
        "orders": orders,
        "beforeOrder": beforeOrder,
        "addresses": addresses,
        "totle_money": totle_money,
    })


def unpaid(request):
    user = getattr(request, 'user', None)
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    beforeOrders = BeforeOrder.objects.filter(status=0, userID_id=user.phoneID)
    return render(request, "tradeweb/unpaid.html",{
        "beforeOrders": beforeOrders,
    })


def topay(request, orderID):
    user = getattr(request, 'user', None)
    beforeOrder = BeforeOrder.objects.get(orderID=orderID)
    orders = Order.objects.filter(beforeOrder=beforeOrder)
    addresses = Address.objects.filter(userID_id=user.phoneID)
    totle_money = 0
    for order in orders:
        totle_money=totle_money+order.goodID.price

    return render(request, "tradeweb/placeOrder.html", {
        "orders": orders,
        "beforeOrder": beforeOrder,
        "addresses": addresses,
        "totle_money":totle_money,
    })


def del_BeforeOrder(request):
    before_OrderID = request.POST["before_OrderID"]
    user = getattr(request, 'user', None)
    beforeOrder = BeforeOrder.objects.get(orderID=before_OrderID)
    orders = Order.objects.filter(beforeOrder=beforeOrder)
    for order in orders:
        good = Goods.objects.get(goodID=order.goodID_id)
        good.state = "在售"
        good.save()
        order.delete()
    beforeOrder.delete()
    return HttpResponseRedirect(reverse("unpaid"))


def payOrder(request):
    if request.method == "POST":
        address = request.POST["address"]
        beforeOrder = request.POST["beforeOrder"]
        beforeOrder = BeforeOrder.objects.get(orderID=beforeOrder)
        orders = Order.objects.filter(beforeOrder=beforeOrder)
        for order in orders:
            good = Goods.objects.get(goodID=order.goodID_id)
            good.state = "已售"
            good.save()
            order.address_id=address
            remark = request.POST["remark_"+str(order.orderID)]
            order.remark = remark
            order.got=0
            order.save()
        beforeOrder.status = 1
        beforeOrder.save()
        return render(request, "tradeweb/pay_success.html")


def got_sure(request):
    if request.method == "POST":
        orderID = request.POST["orderID"]
        order = Order.objects.get(orderID=orderID)
        order.got = 1
        order.save()
        return HttpResponseRedirect(reverse('buyer'))