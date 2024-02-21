from django.db import models
from mapViewer.models import MapPost
from account.models import Member

# Create your models here.
class PostReport(models.Model):
    post = models.ForeignKey(MapPost, on_delete=models.CASCADE)
    reason = models.TextField()

class UserReport(models.Model):
    account = models.ForeignKey(Member, on_delete=models.CASCADE)
    reason = models.TextField()


    