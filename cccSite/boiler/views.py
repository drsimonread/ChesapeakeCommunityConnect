from django.shortcuts import render
from . import models

# Create your views here.
def about(request):
    return render(request, "boiler/about.html")

def help(request):
    return render(request, 'boiler/help.html')

def contact(request):
    if request.method == "POST":
        form = models.messageForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "boiler/thxcontact.html")
    else:
        form=models.messageForm()
    return render(request, "boiler/contact.html", {'form' : form})