from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView
from .models import PostFilters, PostFilterAssoc
from django.db.models import Q
import json

# Create your views here.
#searches simply, based on just a string    
def TextSearch(textRequest):
    results = Entries.objects.filter( Q(entry_name__icontains=textRequest) | Q(entry_desc__icontains=textRequest))
    
    return results

#in particular, this needs to be fed the name of the filters in question, either singular or as a list 
def FilterSearch(filterRequest):
    result_list = []
    results = []
    #get posts if there are no filters
    if filterRequest == "":
        result_list = Entries.objects.all()

    #this way of querying the DB is a little confusing. Basically, because I'm querying a foreign key's related entry, I need to get the association.
    #that's the first line, with the __ representing . or /  a path through associations. then, I'm using association.x.all() because 
    #because the field is many to many, but there's simply a replacement function for the many to one relationship this might be later.
    #If we actually use several associations per filter, I'm not exactly sure how to make useful searches.
    elif isinstance(filterRequest, list):
        for filt in filterRequest:
            association = EntryFilterAssoc.objects.get(Filter_MTM__filter_name__startswith = filt) 
            result_list.append(association.Entry_MTM.all())

    else:
        association = EntryFilterAssoc.objects.get(Filter_MTM__filter_name__startswith = filterRequest) 
        result_list.append(association.Entry_MTM.all())
    

    return result_list