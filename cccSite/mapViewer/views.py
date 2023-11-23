from django.shortcuts import render

# Create your views here.
def viewMap(request):
    return render(request, "mapViewer/mapPage.html")