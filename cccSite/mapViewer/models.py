from django.db import models
from account.models import member

class MapWidget(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Add other fields as needed

# this will be the ideal post model. we would serialize this to widgets using djangos JSON serialize functionality on the specific fields
#class mapPost(models.Model):
#    title = models.CharField(max_length=100)
#    content = models.TextField()
#    author = models.ForeignKey("member", on_delete=models.CASCADE)
#    description = models.TextField() #will be derived from content. whenever this stuff gets working.
#    will need to figure out a good way to store displayable location ie address
#    latitude = models.FloatField()
#    longitude = models.FloatField()