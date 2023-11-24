from django.db import models
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

# Create your models here.
class message(models.Model):
    sender = models.CharField(max_length=75)
    email = models.EmailField()
    subject = models.CharField(max_length=75)
    message = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.sender + " | " + self.email + " | " + self.subject
    
class messageForm(ModelForm):
    class Meta:
        model = message
        fields = ['sender', 'email', 'subject', 'message']
        labels = {
            "sender" : _("Name"),
            "email" : _("Email"),
            "message" : _("Message"),
        }
        widgets = {
            "message": Textarea(attrs={"cols": 40, "rows": 10}),
        }