from django.shortcuts import render, redirect
from django.http import HttpResponse
from boiler.models import Message

# Create your views here.
def default(request):
    return render(request, "Janitor/AdminBase.html")

def messageList(request):
    messages = Message.objects.all()
    return render(request, "Janitor/contactList.html", {'messages' : messages,})
