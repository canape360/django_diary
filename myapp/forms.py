from django import forms
from .models import Diary

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ["title", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "タイトル", "style": "width: 100%;"}),
            "body": forms.Textarea(attrs={"placeholder": "本文", "rows": 8, "style": "width: 100%;"}),
        }
