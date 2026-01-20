from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import views as auth_views

def healthz(request):
    return HttpResponse("ok")

urlpatterns = [
    path("healthz", healthz),

    path("admin/", admin.site.urls),

    # ← 切り分け用に直結
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # これも残す（パスワード変更など全部欲しいなら）
    path("accounts/", include("django.contrib.auth.urls")),

    path("", include("myapp.urls")),
]
