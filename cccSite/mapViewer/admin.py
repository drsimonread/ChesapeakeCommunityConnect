from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Tag)
admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Media)