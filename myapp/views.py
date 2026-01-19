from django.http import HttpResponse

def home(request):
    return HttpResponse("django_diary is running ✅")
