#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
from django import forms
from .models import MapTag
from django.utils.translation import gettext_lazy as _


class SearchPostsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label="Search")
    t = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="Tags")
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }