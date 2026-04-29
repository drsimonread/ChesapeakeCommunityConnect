from django.shortcuts import render
from django.core.mail import send_mail
from . import models

SUPPORT_EMAIL = "cccsitesupport@cccsite.com" # Support email address, should be changed to fit actual support email
NO_REPLY_EMAIL = "noreply@cccsite.com" # No-reply email address, should be changed to fit actual no-reply email


def about(request):
    return render(request, "boiler/about.html")


def _send_contact_notification(message_obj):
    send_mail(
        subject=f"New Contact Message: {message_obj.subject}",
        message=(
            f"Sender: {message_obj.sender}\n"
            f"Email: {message_obj.email}\n\n"
            f"Message:\n{message_obj.message}" # Formats the email content to include the sender's name, email, and the message they submitted
        ),
        from_email=NO_REPLY_EMAIL, # sends from a no-reply email address to avoid direct replies to the support email
        recipient_list=[SUPPORT_EMAIL], # sends to the support email address to ensure it reaches the appropriate team for handling
        fail_silently=False,
    )


def _handle_contact_form(request, form_template): 
    if request.method == "POST":
        form = models.MessageForm(request.POST)
        if form.is_valid():
            message_obj = form.save()
            _send_contact_notification(message_obj)
            return render(request, "boiler/thxcontact.html")
    else:
        form = models.MessageForm()

    return render(request, form_template, {"form": form})


def help(request):
    return _handle_contact_form(request, "boiler/help.html")


def contact(request):
    return _handle_contact_form(request, "boiler/contact.html")