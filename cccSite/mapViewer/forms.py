#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
from django import forms
from django.conf import settings
from .models import Tag
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import googlemaps
from django.db import models
from datetime import datetime
import magic


class SearchForumsForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "map-search-input",
                "placeholder": "Search by title or description…",
                "autocomplete": "off",
            }
        ),
    )
    t = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }



#forum creation form
class MakeForumForm(forms.Form):
    def get_upload_attrs():#function that converts the list of accepted file types to a string for use in restricting what is selectable in the upload interface
        val = '' #start blank
        for item in settings.VALID_UPLOAD_TYPES: #for valid file type
            val = '{0},{1}'.format(val, item) #add to string
        return val
    def validate_file(value): #validator that verifies that uploaded file is of an accepted type. if not, raise validation error
        if magic.from_buffer(value.read(), mime=True) not in settings.VALID_UPLOAD_TYPES:
                raise ValidationError(_("Bad file"), code="filerr")


    title = forms.CharField(
        max_length=100,
        label="Forum title",
        help_text="This is the public name shown on the map, in search, and on the forum page. Keep it short and recognizable.",
        widget=forms.TextInput(
            attrs={
                "class": "cf-control cc-field-input",
                "placeholder": "e.g. Community garden network",
                "autocomplete": "off",
            }
        ),
    )
    firstName = forms.CharField(
        max_length=100,
        label="Your first name",
        help_text="Displayed with this forum as the contact name (same for last name below).",
        widget=forms.TextInput(
            attrs={"class": "cf-control cc-field-input", "placeholder": "First name", "autocomplete": "given-name"}
        ),
    )
    lastName = forms.CharField(
        max_length=100,
        label="Your last name",
        help_text="",
        widget=forms.TextInput(
            attrs={"class": "cf-control cc-field-input", "placeholder": "Last name", "autocomplete": "family-name"}
        ),
    )
    location = forms.CharField(
        max_length=200,
        label="Street address",
        help_text="Start typing; choose a full address from the dropdown so we can place the map pin and store coordinates correctly.",
        widget=forms.TextInput(
            attrs={
                "class": "cf-control cc-field-input",
                "placeholder": "Start typing an address…",
                "autocomplete": "street-address",
            }
        ),
    )
    content = forms.CharField(
        label="Full description",
        help_text="Describe the organization or resource, who it serves, and how others can get involved. You can use multiple paragraphs.",
        widget=forms.Textarea(
            attrs={
                "class": "cf-control cf-control--textarea cc-field-input",
                "placeholder": "Describe the forum, who it serves, and how to get involved.",
                "rows": 8,
            }
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Topic tags",
        help_text="Optional. Select any categories that describe this forum so people can filter and discover it.",
        required=False,
    )
    geoResult = forms.JSONField(widget=forms.HiddenInput, required=False)#hidden field for converting from user provided address to google's geocode

    associated_choices = [
        ("associated", "I am associated with the group providing this solution"),
        ("not-associated", "I am not associated with the group providing this solution")
    ]
    associated = forms.ChoiceField(
        choices=associated_choices,
        widget=forms.RadioSelect(attrs={"class": "cf-radio"}),
        label="Your relationship to this resource",
        help_text="This transparency helps readers trust the information you share.",
    )

    private_public_choices = [
        ("public", "Public — anyone can view and add posts"),
        ("private", "Private — only invited contributors can view and add posts"),
    ]
    private_public = forms.ChoiceField(
        choices=private_public_choices,
        widget=forms.RadioSelect(attrs={"class": "cf-radio"}),
        label="Who can see and post",
        help_text="Public forums are open to all visitors. Private forums are limited to contributors you or moderators invite.",
    )

    file1 = forms.FileField(
        label="File 1",
        help_text="Optional. Upload images or documents allowed by the site (e.g. photos, PDFs).",
        widget=forms.ClearableFileInput(attrs={"accept": get_upload_attrs(), "class": "cf-file-input"}),
        required=False,
        validators=[validate_file],
    )
    file2 = forms.FileField(
        label="File 2",
        help_text="",
        widget=forms.ClearableFileInput(attrs={"accept": get_upload_attrs(), "class": "cf-file-input"}),
        required=False,
        validators=[validate_file],
    )
    file3 = forms.FileField(
        label="File 3",
        help_text="",
        widget=forms.ClearableFileInput(attrs={"accept": get_upload_attrs(), "class": "cf-file-input"}),
        required=False,
        validators=[validate_file],
    )
    file4 = forms.FileField(
        label="File 4",
        help_text="",
        widget=forms.ClearableFileInput(attrs={"accept": get_upload_attrs(), "class": "cf-file-input"}),
        required=False,
        validators=[validate_file],
    )
    

    

    
    #to minimize API calls, we don't want to geocode a provided address more than once. 
    #so if an address is correct, we want to use one geocode call to get the lat/long, but we can't just pass this to the model,
    #because if the provided address doesn't result in a valid geocode, we can't try to access said geocode. this stores a valid geocode
    #in the geoResult field of the form, and  also builds in an error message to the address code if there is no geocode
    def clean(self):
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc') #initialize maps
        cleaned_data = super().clean() #verify that all the other fields are ok
        geoResult = cleaned_data.get("geoResult")
        if not geoResult:
            geoResult = gmaps.geocode(address=cleaned_data["location"])
            if not geoResult:
                raise ValidationError(_("Invalid Address"), code="adderr")
        return {
            "title": cleaned_data["title"],
            "firstName": cleaned_data["firstName"],
            "lastName": cleaned_data["lastName"],
            "location": cleaned_data["location"],
            "content": cleaned_data["content"],
            "tags": cleaned_data["tags"],
            "geoResult": geoResult,
            "associated": cleaned_data["associated"],
            "private_public": cleaned_data["private_public"],
            "files": [
                cleaned_data.get("file1"),
                cleaned_data.get("file2"),
                cleaned_data.get("file3"),
                cleaned_data.get("file4"),
            ],
        }

    def _clean_form(self):
        """Run clean(); map known ValidationError codes to fields, else non-field (avoids silent is_valid bugs)."""
        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            code = getattr(e, "code", None)
            if code == "adderr":
                self.add_error("location", e)
            elif code == "filerr":
                self.add_error("file1", e)
            else:
                self.add_error(None, e)
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data



class SearchPostsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    t = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }




class MakePostForm(forms.Form):
    def get_upload_attrs():#function that converts the list of accepted file types to a string for use in restricting what is selectable in the upload interface
        val = '' #start blank
        for item in settings.VALID_UPLOAD_TYPES: #for valid file type
            val = '{0},{1}'.format(val, item) #add to string
        return val
    def validate_file(value): #validator that verifies that uploaded file is of an accepted type. if not, raise validation error
        if magic.from_buffer(value.read(), mime=True) not in settings.VALID_UPLOAD_TYPES:
                raise ValidationError(_("Bad file"), code="filerr")


    title = forms.CharField(max_length=100, label="Title", widget=forms.TextInput({"Placeholder": "Title"})) #title of forum
    firstName = forms.CharField(max_length=100, label="First", widget=forms.TextInput({"Placeholder": "First"})) #first name of author of forum
    lastName = forms.CharField(max_length=100, label="Last", widget=forms.TextInput({"Placeholder": "Last"})) #last name of author of forum
    location = forms.CharField(max_length=200, label="Address", widget=forms.TextInput({"Placeholder": "Location"})) #location of forum as an address
    content = forms.CharField(label="Content", widget=forms.Textarea({"Placeholder": "Content"})) #content of the forum
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tags", required = False)#tags of forum
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









class SearchCommentsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    t = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }




class MakeCommentsForm(forms.Form):
    def get_upload_attrs():#function that converts the list of accepted file types to a string for use in restricting what is selectable in the upload interface
        val = '' #start blank
        for item in settings.VALID_UPLOAD_TYPES: #for valid file type
            val = '{0},{1}'.format(val, item) #add to string
        return val
    def validate_file(value): #validator that verifies that uploaded file is of an accepted type. if not, raise validation error
        if magic.from_buffer(value.read(), mime=True) not in settings.VALID_UPLOAD_TYPES:
                raise ValidationError(_("Bad file"), code="filerr")


    content = forms.CharField(label="Content", widget=forms.Textarea({"Placeholder": "Content"})) #content of the forum
    

    def clean(self): 
        # gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc') #initialize maps
        cleaned_data = super().clean() #verify that all the other fields are ok
        # if not cleaned_data['geoResult']: #if we don't have a geocode (first try or last try was invalid)
            # geoResult=gmaps.geocode(address=self.cleaned_data['location']) #fetch geocode for provided address (API call)
            # if not geoResult: #if still none, then the address is invalid
                # raise ValidationError(_("Invalid Address"), code="adderr")
        #print(geoResult)
        return {'content': cleaned_data['content']
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
                # case "filerr":
                    # self.add_error('file1', e) #if we get a file error, attach it to the first file field.
            
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data #if successful, store in cleaned_data





