from django.db import models
import datetime
from mapViewer.models import MapWidget
# Create your models here.

class PostFilters(models.Model):
    filter_name = models.CharField(max_length=200)
    filter_desc = models.CharField(max_length=1000)
    def __str__(self):
        return self.filter_name
#

#seperate table for associations, should only use this table for Filter
class PostFilterAssoc(models.Model):
    AssociationName = models.CharField(max_length=200)
    Entry_MTM = models.ManyToManyField(MapWidget)
    Filter_MTM = models.ManyToManyField(PostFilters)
    def __str__(self):
        return self.AssociationName
