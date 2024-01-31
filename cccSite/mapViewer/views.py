from django.core import serializers
from django.shortcuts import render
from .models import MapWidget
from Filterer.views import TextSearch, FilterSearch

from django.http import JsonResponse
from .models import Widget
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

@csrf_exempt
def save_widget(request):
    if request.method == 'POST':
        # Extract data from request and save widget
        widget = Widget(
            title=request.POST['title'],
            description=request.POST['description'],
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude']
        )
        widget.save()
        return JsonResponse({'status': 'success'})

def search_widgets(request):
    # Implement search logic and return results
    # For example, search by title:
    search_text = request.GET.get('searchText', '')
    widgets = Widget.objects.filter(title__icontains=search_text)
    data = serializers.serialize('json', widgets)
    return JsonResponse({'widgets': data})

def viewMap(request):
    widgets = serializers.serialize('json', MapWidget.objects.all())
    print(widgets)  # Temporary print statement to check the output
    return render(request, 'mapViewer/mapPage.html', {'widgets': widgets})

def mapSearch(request):
    if (request.GET.get('searchBtn')):
        searchText = request.GET.get('search-text')
        return JsonResponse({"status":"success"})
    return JsonResponse({"status": "error"}, status = 400)
