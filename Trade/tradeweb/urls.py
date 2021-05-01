from django.urls import path
from django.views.static import serve

from Trade.settings import MEDIA_ROOT
from tradeweb import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("student", views.student, name="student"),
    path("ajax_school", views.ajax_school),
    path("media/<slug:path>", serve, {"document_root":MEDIA_ROOT}),
    path("release", views.release, name="release"),
    path("details/<int:goodID>", views.details, name="details"),
    path("ajax_comment", views.ajax_comment),
    path("ajax_want", views.ajax_want),
    path("ajax_nick", views.ajax_nick),
    path("ajax_mail", views.ajax_mail),
    path("ajax_deladdress", views.ajax_deladdress),
    path("add_address", views.add_address,name="add_address"),
    path("infopage", views.infopage, name="infopage"),
    path("address", views.address, name="address"),
    path('message', views.message, name="message"),
    path("shopping_car", views.shopping_car, name="shopping_car"),
    path("buyer", views.buyer, name="buyer"),
    path("delwantgoods", views.delwantgoods,name="delwantgoods"),
    path("bebought", views.bebought, name="bebought"),
    path("placeOrder/<slug:url>", views.placeOrder, name="placeOrder"),
    path("unpaid", views.unpaid, name="unpaid"),
    path("topay/<int:orderID>", views.topay, name="topay"),
    path("del_BeforeOrder", views.del_BeforeOrder, name="del_BeforeOrder"),
    path("payOrder", views.payOrder, name="payOrder"),
    path("got_sure", views.got_sure, name="got_sure"),

]