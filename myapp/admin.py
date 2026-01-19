from django.contrib import admin
from .models import Person, Diary, MyMail


class DiaryInline(admin.TabularInline):  # 表形式。フォームっぽくしたいなら StackedInline
    model = Diary
    extra = 1  # 追加フォームを最初に何個出すか
    fields = ("title", "body", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    search_fields = ("name", "email")
    inlines = [DiaryInline]


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "person", "created_at")
    list_filter = ("created_at", "person")
    search_fields = ("title", "body")


@admin.register(MyMail)
class MyMailAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "person", "sent_at")
    list_filter = ("sent_at", "person")
    search_fields = ("subject", "body")
