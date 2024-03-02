from django.forms import Form, ModelForm
from django import forms
from account.models import Member
from mapViewer.models import MapTag

class TagRemover(Form):
    tags = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tags")

class TagAdder(ModelForm):
    class Meta:
        model = MapTag
        fields = ['name']
