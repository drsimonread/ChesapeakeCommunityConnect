from django.core import serializers
from django.shortcuts import render
from .models import MapWidget
from Filterer.views import TextSearch, FilterSearch

def save_widget(request):
    if request.method == "POST":
        MapWidget.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude')
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def viewMap(request):
    widgets = serializers.serialize('json', MapWidget.objects.all())
    print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets})

def search_widgets(request):
    if (request.GET.get('searchBtn')):
        searchText = request.GET.get('search-text')
        return JsonResponse({"status":"success"})
    return JsonResponse({"status": "error"}, status = 400)
