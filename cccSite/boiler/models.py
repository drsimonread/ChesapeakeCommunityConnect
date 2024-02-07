from django.db import models
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=75)
    email = models.EmailField()
    subject = models.CharField(max_length=75)
    message = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.sender + " | " + self.email + " | " + self.subject
    
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'email', 'subject', 'message']
        labels = {
            "sender": _("Name"),
            "email": _("Email"),
            "message": _("Message"),
        }
        widgets = {
            'sender': TextInput(attrs={'placeholder': 'Name', 'class': 'input-text'}),
            'email': EmailInput(attrs={'placeholder': 'Email address', 'class': 'input-text'}),
            'subject': TextInput(attrs={'placeholder': 'Subject', 'class': 'input-text'}),
            'message': Textarea(attrs={'placeholder': 'Message', 'class': 'input-textarea'}),
        }