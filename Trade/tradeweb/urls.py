from django.urls import path

from tradeweb import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("student", views.student, name="student"),
    path("ajax_school", views.ajax_school),
]