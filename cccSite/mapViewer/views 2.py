from django.core import serializers
from django.shortcuts import render
from .models import MapWidget
from django.http import JsonResponse

def save_widget(request):
    if request.method == "POST":
        try:
            MapWidget.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude')
            )
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error"}, status=400)


def viewMap(request):
    widgets = serializers.serialize('json', MapWidget.objects.all())
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets})
