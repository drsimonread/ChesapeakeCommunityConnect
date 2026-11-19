from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PostReport)
admin.site.register(CommentReport)
admin.site.register(UserReport)