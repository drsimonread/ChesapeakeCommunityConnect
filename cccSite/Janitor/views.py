from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def default(request):
    return render(request, "Janitor/AdminBase.html")

def messageList(request):
    return render(request, "Janitor/AdminBase.html")
