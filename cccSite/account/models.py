from django.db import models
from django.forms import ModelForm
from .storage import OverwriteStorage



def user_directory_profile(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    ext = filename.split('.')[-1]
    filename="profile."+ext
    return 'users/{0}/{1}'.format(instance.pk, filename) 

# Create your models here.
class member(models.Model):
    userID = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=35)
    ranking = models.CharField(max_length=20, default="member")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    email = models.EmailField()
    origin = models.CharField(max_length=10, default="userpass")
    pic = models.ImageField(upload_to=user_directory_profile, storage = OverwriteStorage(), null=True, blank=True)
    about = models.TextField(blank=True, default="")
   #location = AddressField(blank=True, default={"raw" : ""}, null=True)
    def __str__(self):
        return self.name + "|" + self.userID
    #https://stackoverflow.com/questions/3715103/password-field-in-django-model/3715382#3715382 for making own password

class manageForm(ModelForm):
    class Meta:
        model = member
        fields = ["pic", "name", "email", "about"]
