"""
URL configuration for cccSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    #path("map/", include("mapViewer.urls")),
    path("account/", include("account.urls")),
    path('DJadmin/', admin.site.urls),
    path("", include("mapViewer.urls")),
    path("", include("boiler.urls")),
    path("admin/", include("Janitor.urls")),
    # django.conf.urls.static.static() adds no route when DEBUG is False.
    re_path(rf"^{re.escape(settings.MEDIA_URL.lstrip('/'))}(?P<path>.*)$", serve,
            {"document_root": settings.MEDIA_ROOT}),
]
