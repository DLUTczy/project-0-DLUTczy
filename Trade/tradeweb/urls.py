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
    path("release/<int:phoneID>", views.release, name="release")
]