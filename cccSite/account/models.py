from django.db import models
from django.forms import ModelForm
from .storage import OverwriteStorage


#function used for saving images
def user_directory_profile(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / user_<id> / <filename> 
    ext = filename.split('.')[-1]
    filename="profile."+ext
    return 'users/{0}/{1}'.format(instance.pk, filename) 

# user model. self explanitory
class member(models.Model):
    userID = models.CharField(max_length=255, unique=True) #this will be deleted eventually, but right now this stores the google ID
    name = models.CharField(max_length=35)
    ranking = models.CharField(max_length=20, default="member")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    email = models.EmailField()
    pic = models.ImageField(upload_to=user_directory_profile, storage = OverwriteStorage(), default='default/blankprof.png')
    about = models.TextField(blank=True, default="")
   #location = AddressField(blank=True, default={"raw" : ""}, null=True)
    def __str__(self):
        return self.name + "|" + self.userID
    #https://stackoverflow.com/questions/3715103/password-field-in-django-model/3715382#3715382 for making own password


# not implemented yet
# when user logs in with google, check the given google ID against this and then authenticate as user that is pointed to
# same pattern can be used to implement other log in methods
class gLogIn(models.Model):
    googleID = models.CharField(max_length=255, unique=True)
    pointTo = models.ForeignKey("member", on_delete = models.CASCADE)

class manageForm(ModelForm):
    class Meta:
        model = member
        fields = ["pic", "name", "email", "about"]
