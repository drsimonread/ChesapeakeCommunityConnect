from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import CreateAccountForm, SearchAccountForm
from django.db.models import Count
from django.db.models import Q
import json
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from PIL import Image
from .models import Member, GLogIn

# YOUR SPECIFIC CLIENT ID
GOOGLE_CLIENT_ID = "909497695712-h9smcju9klvlqk70celohtne9o438htn.apps.googleusercontent.com"

def google_signin(request):
    if request.method == "POST":
        token = request.POST.get("credential", "")

        try:
            # 1. Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GOOGLE_CLIENT_ID
            )

            google_id = idinfo["sub"]  # Google's unique user ID
            email = idinfo.get("email", "")
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")

            # 2. Check if this GoogleID already exists
            try:
                glog = GLogIn.objects.get(googleID=google_id)
                member = glog.referTo
                user = member.user

            except GLogIn.DoesNotExist:
                # 3. Create or get Django User based on email
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )

                # 4. Create Member if not exists
                member, created_member = Member.objects.get_or_create(
                    user=user,
                    defaults={"ranking": 1}
                )

                # 5. Store mapping GoogleID → Member
                GLogIn.objects.create(
                    googleID=google_id,
                    referTo=member
                )

            # 6. Log them in using Django
            login(request, user)

            # 7. Set your custom session keys
            request.session["rank"] = member.ranking
            request.session["user"] = member.pk
            request.session["name"] = user.username

            return JsonResponse({"success": True})

        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid token"}, status=400)

    return JsonResponse({"success": False}, status=405)
from mapViewer.models import MapPost
from .forms import CreateForumForm, SearchAccountForm
from urllib.parse import urlencode
from string import ascii_uppercase

# if user not signed in, sends them to log in 
def signin(request):
    if request.session.get('rank', 0)==0:
        return render(request, 'account/signin.html')
    else:
        return redirect("/account/")

# if a user tries to sign out by URL, redirects to account. if there is a POST request to this url, flushes the session and sends them to confirmation
def signout(request):
    if request.method == "POST":
        request.session.flush()
    return redirect(reverse("account:default"))

 
 # default account page. send to sign in if not signed in, otherwise displays user info
def default(request):
    if request.session.get('rank',0)==0:
        return redirect(reverse("account:signin"))
    else:
        userInz=Member.objects.get(pk=request.session['user']) #get user from session
        visible_posts = MapPost.objects.filter(
            author=userInz, visibility=1
        ).order_by("-created")
        return render(request, 'account/myaccount.html', {
            'name': userInz.name,
            'email' : userInz.email,
            'image' : userInz.pic,
            'about' : userInz.about,
            'visible_posts': visible_posts,
        })
    
def account_all(request):
    return HttpResponse("insert account view list here")
    search = SearchAccountForm(request.GET)
    query = request.GET.get("q", "").strip()
    letter = request.GET.get("letter", "").strip().upper()
    if letter not in ascii_uppercase:
        letter = ""
    sort = request.GET.get("s", "0")
    page_number = request.GET.get("page", "1")

    members = Member.objects.annotate(
        num_forums=Count(
            "mappost",
            filter=Q(mappost__visibility=1),
        ),
    ).filter(num_forums__gt=0)
    if query:
        members = members.filter(name__icontains=query)
    if letter:
        members = members.filter(name__istartswith=letter)

    sort_fields = {
        "0": ("name",),
        "1": ("-name",),
        "2": ("-num_forums", "name"),
        "3": ("num_forums", "name"),
    }
    sort = sort if sort in sort_fields else "0"
    members = members.order_by(*sort_fields[sort])
    page_obj = Paginator(members, 20).get_page(page_number)

    def query_string(**updates):
        values = {"q": query, "letter": letter, "s": sort, "page": page_obj.number}
        values.update(updates)
        return "?" + urlencode({key: value for key, value in values.items() if value not in ("", None)}
                               )

    return render(request, "account/account_list.html", {
        "is_signed_in": request.session.get("rank", 0) > 0,
        "search": search,
        "search_query": query,
        "selected_letter": letter,
        "letter_links": [
            {"letter": alphabet_letter, "url": query_string(letter=alphabet_letter, page=1)}
            for alphabet_letter in ascii_uppercase
        ],
        "sort_value": sort,
        "page_obj": page_obj,
        "qs_clear_search": query_string(q="", page=1),
        "qs_reset": query_string(q="", letter="", s="0", page=1),
        "qs_sort_az": query_string(s="0", page=1),
        "qs_sort_za": query_string(s="1", page=1),
        "qs_sort_forums_hi": query_string(s="2", page=1),
        "qs_sort_forums_lo": query_string(s="3", page=1),
        "qs_prev": query_string(page=page_obj.previous_page_number() if page_obj.has_previous() else 1),
        "qs_next": query_string(page=page_obj.next_page_number() if page_obj.has_next() else page_obj.number),
    })
    
def account_view(request, want):
    if not want:
        return HttpResponse("Insert list view here")
    if not Member.objects.get(pk=want):
        return redirect(reverse("account:default"))
    viewInz=Member.objects.get(pk=want)
    if request.session.get('rank',0) != 0:
        userInz=Member.objects.get(request.session['user'])
    else:
        userInz= Member.objects.none()
    
    view_inz = get_object_or_404(Member, pk=want)
    return render(request, "account/profile.html", {
        "profile": view_inz,
        "visible_posts": MapPost.objects.filter(
            author=view_inz, visibility=1
        ).order_by("-created"),
    })
    

# the username/password account that belongs to a signed-in member, or None if they only sign in with Google.
# members and their password accounts are linked by email, the same way signin_form links them
def password_account_for(member):
    return AccountCreation.objects.filter(email__iexact=member.email, status="accepted").first()

# checks the change password form and returns an error message, or None if the new password can be saved
def password_change_error(account, current, new, confirm):
    if not (current and new and confirm):
        return "Fill in all three password fields."
    if account.password != current:
        return "Your current password is incorrect."
    if new != confirm:
        return "The new passwords do not match."
    if new == current:
        return "Your new password must be different from your current password."
    if len(new) < 8:
        return "Your new password must be at least 8 characters long."
    max_length = AccountCreation._meta.get_field("password").max_length
    if len(new) > max_length:
        return f"Your new password must be at most {max_length} characters long."
    return None

# lets members edit their info
def manage(request):
    if request.session.get('rank',0)==0:
        return redirect('/account/signin/')
    if request.method == "POST":
        userInz=Member.objects.get(pk=request.session['user']) 
        form = ManageForm(request.POST, request.FILES, instance=userInz)
        if form.is_valid():
            form.save()
            request.session['name']=userInz.name
            return redirect("/account/")
    else:
        userInz=Member.objects.get(pk=request.session['user'])
        form = ManageForm(instance=userInz)
    return render(request, "account/manage.html", {'form' : form})

# a lot of this code is from google btw. this view verifies google one touch log in credentials
#view for creating forums
def make_forum(request):
    if(request.session.get('rank',0) == 0): #if user is not signed in, require sign in
        return redirect(reverse("account:signin"))
    if(request.method=="POST"): #if the request was a post, it is an attempt to create a forum
        contentForm= MakeForumForm(request.POST, request.FILES) #create the posting form instance and populate it with the data in the POST request
        if contentForm.is_valid(): #if the forum is good to go, calls the clean method and validators from MakeForumForm in mapViewer/forms.py
            # MEMBER_DELETE
            userInz=Member.objects.get(pk=request.session['user']) #get user's member instance from session
            if len(contentForm.cleaned_data['content']) > 35: #if content overflows the preview length
                disc = contentForm.cleaned_data['content'][slice(0,35)] + "..." #create description to act as a preview
            else:
                disc = contentForm.cleaned_data['content'] #otherwise just use content to describe #? Why does description exist at all?
            vis=0 #default visibility set to pending
            if request.session['rank'] > 1: #if user is trusted, set visibility to visible
                vis=1
            forumInz=Forum.objects.create(title=contentForm.cleaned_data['title'], #actually create the forum instance in the database
                                   content=contentForm.cleaned_data['content'],
                                   firstName=contentForm.cleaned_data['firstName'],
                                   lastName=contentForm.cleaned_data['lastName'],
                                   author=userInz,
                                   description=disc,
                                   geoCode=contentForm.cleaned_data['geoResult'][0],
                                   visibility=vis,
                                   associated=contentForm.cleaned_data['associated'],
                                   private_public=contentForm.cleaned_data['private_public']
                                   )
            if contentForm.cleaned_data['tags']: #if there are any tags
                forumInz.tags.set(contentForm.cleaned_data['tags']) #set the forum's tags according to selected tags
            
            if contentForm.cleaned_data['files']: #if there are files uploaded
                for item in contentForm.cleaned_data['files']: #iterates through file upload fields
                    if item != None: #if item is none, then nothing was uploaded
                        fileInz = Media.objects.create(forum=forumInz, file=item) #create a forumfile instance
                        fileInz.format = fileInz.get_format() #get the format and set the format
                        fileInz.save() #save the updated format
            return redirect(reverse('mapViewer:forum_detail', args=[forumInz.pk])) #redirect to the forum view of the just posted forum
            
    else:
        contentForm = MakeForumForm()
    return render(request, 'account/create_forum.html', {'form': contentForm,})
