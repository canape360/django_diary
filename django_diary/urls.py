from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def healthz(request):
    return HttpResponse("ok")


urlpatterns = [
    # Render Health Check 用（必ず 200 を返す）
    path("healthz", healthz),

    # Django Admin
    path("admin/", admin.site.urls),

    # Django 標準ログイン / ログアウト
    path("accounts/", include("django.contrib.auth.urls")),

    # アプリのURL（トップページ含む）
    path("", include("myapp.urls")),
]
