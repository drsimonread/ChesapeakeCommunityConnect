from django.db import models
from account.models import Member
from django.urls import reverse

class MapWidget(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Add other fields as needed



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
#    will need to figure out a good way to store displayable location ie address
    geoCode = models.JSONField()
    tags = models.ManyToManyField(MapTag, related_name="posts", blank=True)
    isVisible = models.BooleanField(default=False)
    def __str__(self):
        return self.title + " by " + str(self.author)
    def get_absolute_url(self):
        return reverse("mapViewer:post_detail", args=[str(self.pk)])
    
    #https://forum.djangoproject.com/t/url-template-tag-get-absolute-url-and-views/21249
    #https://levelup.gitconnected.com/django-quick-tips-get-absolute-url-1c22321f806b
