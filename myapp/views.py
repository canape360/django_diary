# myapp/views.py
# myapp/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DiaryForm
from .models import Diary


def signup(request):
    """招待制サインアップ（SIGNUP_CODE が空なら合言葉チェックなしで登録可）"""
    if request.user.is_authenticated:
        return redirect("myapp:wholediary")

    if request.method == "POST":
        # 合言葉（招待コード）
        code = request.POST.get("signup_code", "").strip()
        required_code = getattr(settings, "SIGNUP_CODE", "").strip()

        if required_code and code != required_code:
            messages.error(request, "合言葉が違います。")
            form = UserCreationForm(request.POST)
            return render(request, "registration/signup.html", {"form": form})

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後にログイン状態にする
            return redirect("myapp:wholediary")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def privacy(request):
    return render(request, "privacy.html")


def disclaimer(request):
    return render(request, "disclaimer.html")


def home(request):
    return render(request, "home.html")


@login_required
def wholediary(request):
    diaries = Diary.objects.filter(user=request.user)
    return render(request, "wholediary.html", {"diaries": diaries})


@login_required
def diary_create(request):
    if request.method == "POST":
        form = DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.user = request.user
            diary.save()
            return redirect("myapp:wholediary")
    else:
        form = DiaryForm()

    return render(request, "diary_create.html", {"form": form})


@login_required
def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk, user=request.user)
    return render(request, "diary_detail.html", {"diary": diary})


@login_required
def diary_edit(request, pk):
    diary = get_object_or_404(Diary, pk=pk, user=request.user)

    if request.method == "POST":
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            form.save()
            return redirect("myapp:diary_detail", pk=diary.pk)
    else:
        form = DiaryForm(instance=diary)

    return render(request, "diary_edit.html", {"form": form, "diary": diary})


@login_required
def diary_delete(request, pk):
    diary = get_object_or_404(Diary, pk=pk, user=request.user)

    if request.method == "POST":
        diary.delete()
        return redirect("myapp:wholediary")

    return render(request, "diary_delete.html", {"diary": diary})
