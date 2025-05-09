from django.forms import Form, ModelForm
from django import forms
from account.models import Member
from mapViewer.models import MapTag
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

class MemberManager(ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'ranking', 'email','pic','about']

