# myapp/urls.py
from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("wholediary/", views.wholediary, name="wholediary"),

    path("diary/new/", views.diary_create, name="diary_create"),
    path("diary/<int:pk>/", views.diary_detail, name="diary_detail"),
    path("diary/<int:pk>/edit/", views.diary_edit, name="diary_edit"),
    path("diary/<int:pk>/delete/", views.diary_delete, name="diary_delete"),

    path("privacy/", views.privacy, name="privacy"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),

    path("accounts/signup/", views.signup, name="signup"),
]
