from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Diary, MyMail

User = get_user_model()


class DiaryInline(admin.TabularInline):
    model = Diary
    extra = 1
    fields = ("title", "body", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


class MyMailInline(admin.TabularInline):
    model = MyMail
    extra = 0
    fields = ("subject", "sent_at")
    readonly_fields = ("sent_at",)
    show_change_link = True


# 既存のUser管理画面に、Diary / MyMail をインライン追加
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = [DiaryInline, MyMailInline]


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("title", "body", "user__username")


@admin.register(MyMail)
class MyMailAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "user", "sent_at")
    list_filter = ("sent_at", "user")
    search_fields = ("subject", "body", "user__username")
