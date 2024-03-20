from django.db import models
from django.forms import ModelForm
from account.models import Member
from multiupload.fields import MultiMediaField
from django.urls import reverse
from uuid import uuid4


class MapTag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    def __str__(self):
        return self.name

# this will be the ideal post model. we would serialize this to widgets using djangos JSON serialize functionality on the specific fields
class MapPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    description = models.TextField() #will be derived from content. whenever this stuff gets working.
    geoCode = models.JSONField()
    tags = models.ManyToManyField(MapTag, related_name="posts", blank=True)
    visible_options = { 
        (-1,"denied"),
        (0, "pending"),
        (1 , "visible"),
    }
    visibility = models.SmallIntegerField(default=0, choices=visible_options)
    def __str__(self):
        return self.title + " by " + str(self.author)
    @property
    def get_absolute_url(self):
        return reverse("mapViewer:post_detail", args=[str(self.pk)])
    
    #https://forum.djangoproject.com/t/url-template-tag-get-absolute-url-and-views/21249
    #https://levelup.gitconnected.com/django-quick-tips-get-absolute-url-1c22321f806b

def post_file_directory(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / posts / <post.pk> / <pk>.<ext>
    ext = filename.split('.')[-1]
    filename="{0}.".format(uuid4().hex)+ext
    return 'posts/{0}/{1}'.format(instance.post.pk, filename) 




class PostFile(models.Model):
    post = models.ForeignKey(MapPost, on_delete=models.CASCADE)
    format_options = { 
        (0, "image"),
        (1, "video"),
        (2 , "audio"),
    }
    format = models.SmallIntegerField(default=0, choices=format_options)
    file = models.FileField(upload_to=post_file_directory)
    def get_format(self):
        extension = self.file.url.split('.')[-1]
        match extension:
            case "jpg":
                return 0
            case "mp4":
                return 1
            case "mp3":
                return 2
            
