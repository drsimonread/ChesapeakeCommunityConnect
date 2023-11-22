from django.db import models

# Create your models here.
class member(models.Model):
    userID = models.CharField(max_length=255)
    first = models.CharField(max_length=35)
    last = models.CharField(max_length=35)
    ranking = models.CharField(max_length=20, default="member")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    email = models.EmailField()
    def __str__(self):
        return self.first + "|" + self.userID