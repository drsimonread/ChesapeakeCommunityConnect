from django.forms import Form, ModelForm
from django import forms
from account.models import Member
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from mapViewer.models import MapTag, MapPost
from .models import *

class TagRemover(Form):
    tags = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tags")

class TagAdder(ModelForm):
    class Meta:
        model = MapTag
        fields = ['name']

class UserRepForm(ModelForm):
    class Meta:
        model = UserReport
        fields = ['reason', 'account']
        widgets = {
            'account' : forms.HiddenInput,
        }

class PostRepForm(ModelForm):
    class Meta:
        model = PostReport
        fields = ['reason', 'post']
        widgets = {
            'post' : forms.HiddenInput,
        }

class PostManager(ModelForm):
    reason = forms.CharField(label="Reason", widget=forms.Textarea, required=False)
    class Meta:
        model = MapPost
        fields = ['visibility', 'description']
        widgets={
            'description' : forms.HiddenInput
        }
    def clean(self): 
        cleaned_data = super().clean() #verify that all the other fields are ok
        if cleaned_data.get('visibility')==-1: #if visibility has been set to blocked
            if not cleaned_data.get('reason'): #make sure a reason was provided
                raise ValidationError(_("You must include a reason."), code="reaserr")
            else: #if it was provided, set the description to the reason so the user knows.
                cleaned_data = {'reason' : cleaned_data.get('reason'),
                                'visibility' : cleaned_data.get('visibility'),
                                'description' : cleaned_data.get('reason')}
        return cleaned_data
        
    def _clean_form(self): #when we check is_valid, this occurs
        try:
            cleaned_data = self.clean() #try to clean the data
        except ValidationError as e:
            match e.code:
                case "reaserr":
                    self.add_error('reason', e)
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data #if successful, store in cleaned_data
    
    

class MemberManager(ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'ranking', 'email','pic','about']

