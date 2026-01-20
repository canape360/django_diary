from django.contrib import admin
from django.urls import path
from myapp.views import home
from django.http import HttpResponse


def healthz(request):
    return HttpResponse("ok")

urlpatterns = [
    path("healthz", healthz),
    # 既存の urls...
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
]
