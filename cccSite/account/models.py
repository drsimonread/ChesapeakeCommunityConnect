from django.db import models

# Create your models here.
class member(models.Model):
    userID = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=35)
    ranking = models.CharField(max_length=20, default="member")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    email = models.EmailField()
    origin = models.CharField(max_length=10, default="userpass")
    pic = models.ImageField(upload_to='{0}/profile'.format(userID), null=True)
    about = models.CharField(max_length=255, blank=True, default="")
    def __str__(self):
        return self.first + "|" + self.userID
    #https://stackoverflow.com/questions/3715103/password-field-in-django-model/3715382#3715382 for making own password


