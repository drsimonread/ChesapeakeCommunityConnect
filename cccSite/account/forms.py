from django import forms

class CreateAccountForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput({'Placeholder' : "User Name"}))
    email = forms.EmailField(widget=forms.TextInput({'Placeholder' : "Email"}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput({'Placeholder' : "Password"}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput({'Placeholder' : "Confirm Password"}))
    