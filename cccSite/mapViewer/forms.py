#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
from django import forms
from django.conf import settings
from .models import MapTag
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import googlemaps
from django.db import models
from datetime import datetime
import magic


def get_upload_attrs():
    valid_types = getattr(settings, "VALID_UPLOAD_TYPES", ())
    return ",".join(valid_types)


def validate_file(value):
    valid_types = getattr(settings, "VALID_UPLOAD_TYPES", ())
    if valid_types and magic.from_buffer(value.read(), mime=True) not in valid_types:
        raise ValidationError(_("Bad file"), code="filerr")


class SearchForumsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    t = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }



#forum creation form
class MakeForumForm(forms.Form):
    def get_upload_attrs():#function that converts the list of accepted file types to a string for use in restricting what is selectable in the upload interface
        val = '' #start blank
        valid_types = getattr(settings, "VALID_UPLOAD_TYPES", ())
        for item in valid_types: #for valid file type
            val = '{0},{1}'.format(val, item) #add to string
        return val
    def validate_file(value): #validator that verifies that uploaded file is of an accepted type. if not, raise validation error
        valid_types = getattr(settings, "VALID_UPLOAD_TYPES", ())
        if valid_types and magic.from_buffer(value.read(), mime=True) not in valid_types:
                raise ValidationError(_("Bad file"), code="filerr")


    title = forms.CharField(max_length=100, label="Title", widget=forms.TextInput({"Placeholder": "Title"})) #title of forum
    firstName = forms.CharField(max_length=100, label="First", widget=forms.TextInput({"Placeholder": "First"})) #first name of author of forum
    lastName = forms.CharField(max_length=100, label="Last", widget=forms.TextInput({"Placeholder": "Last"})) #last name of author of forum
    location = forms.CharField(max_length=200, label="Address", widget=forms.TextInput({"Placeholder": "Location"})) #location of forum as an address
    content = forms.CharField(label="Content", widget=forms.Textarea({"Placeholder": "Content"})) #content of the forum
    tags = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tags", required = False)#tags of forum
    geoResult = forms.JSONField(widget=forms.HiddenInput, required=False)#hidden field for converting from user provided address to google's geocode
    
    associated_choices = [
        ("associated", "I am associated with the group providing this solution"),
        ("not-associated", "I am not associated with the group providing this solution")
    ]
    associated = forms.ChoiceField(choices=associated_choices)
    
    private_public_choices = [
        ("public", "Public (Anyone can view and add Posts)"),
        ("private", "Private (Only invited Contributors can view and add Posts)")
    ]
    private_public = forms.ChoiceField(choices=private_public_choices)
    
    
    #the file upload fields. validated using the custom validator above, if left empty or if a bad file is submitted, these fields have nothing in them
    file1 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    file2 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    file3 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    file4 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    

    

    
    #to minimize API calls, we don't want to geocode a provided address more than once. 
    #so if an address is correct, we want to use one geocode call to get the lat/long, but we can't just pass this to the model,
    #because if the provided address doesn't result in a valid geocode, we can't try to access said geocode. this stores a valid geocode
    #in the geoResult field of the form, and  also builds in an error message to the address code if there is no geocode
    def clean(self): 
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc') #initialize maps
        cleaned_data = super().clean() #verify that all the other fields are ok
        if not cleaned_data['geoResult']: #if we don't have a geocode (first try or last try was invalid)
            geoResult=gmaps.geocode(address=self.cleaned_data['location']) #fetch geocode for provided address (API call)
            if not geoResult: #if still none, then the address is invalid
                raise ValidationError(_("Invalid Address"), code="adderr")
        #print(geoResult)
        return {'title': cleaned_data['title'],
                'firstName': cleaned_data['firstName'],
                'lastName': cleaned_data['lastName'],
                'location': cleaned_data['location'],
                'content': cleaned_data['content'],
                'tags': cleaned_data['tags'],
                'geoResult': geoResult,
                'associated': cleaned_data['associated'],
                'private_public': cleaned_data['private_public'],
                'files': [cleaned_data.get('file1'),cleaned_data.get('file2'),cleaned_data.get('file3'),cleaned_data.get('file4')],
                }  # if a file is legit, the .get returns the file. if not (or if it doesn't exist), 
                # the .get returns None, and so we can iterate through cleaned_data['files'] in a view, and check if an entry isn't None to 
                # see if we have a file to save or not
        
    def _clean_form(self): #when we check is_valid, this occurs
        try:
            cleaned_data = self.clean() #try to clean the data
        except ValidationError as e:
            match e.code:
                case "adderr":
                    self.add_error('location', e) #if we get the error of invalid address, attach it to the location field
                case "filerr":
                    self.add_error('file1', e) #if we get a file error, attach it to the first file field.
            
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data #if successful, store in cleaned_data



class SearchPostsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    t = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }


class GuestPostForm(forms.Form):
    email = forms.EmailField(
            max_length=254,
            label="Email",
            widget=forms.EmailInput(attrs={
                "id": "email",
                "autocomplete": "email",
            }),
    )
    title = forms.CharField(max_length=100, label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    address = forms.CharField(max_length=200, label="Address")
    city = forms.CharField(max_length=100, required=False, label="City")
    state = forms.CharField(max_length=100, required=False, label="State")
    zipcode = forms.CharField(max_length=20, required=False, label="Zipcode")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("title", "description", "address", "city", "state", "zipcode"):
            self.fields[field_name].widget.attrs["id"] = field_name


class MakePostForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    location = forms.CharField(max_length=200, label="Address", widget=forms.TextInput)
    content = forms.CharField(label="Content", widget=forms.Textarea)
    tags = forms.ModelMultipleChoiceField(
        queryset=MapTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Tags",
        required=False,
    )
    geoResult = forms.JSONField(widget=forms.HiddenInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get("location")
        if self.errors or cleaned_data.get("geoResult"):
            return cleaned_data

        if not settings.GOOGLE_API_KEY:
            self.add_error("location", _("Address lookup is unavailable."))
            return cleaned_data

        results = googlemaps.Client(key=settings.GOOGLE_API_KEY).geocode(address=location)
        if results:
            cleaned_data["geoResult"] = results
        else:
            self.add_error("location", ValidationError(_("Invalid Address"), code="adderr"))
        return cleaned_data


class PostCommentForm(forms.Form):
    content = forms.CharField(
        label="",
        max_length=10000,
        widget=forms.Textarea(attrs={
            "placeholder": "Share your thoughts...",
            "rows": 4,
        }),
    )
