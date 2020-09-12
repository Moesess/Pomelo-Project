from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from choices import *


class ContactForm(forms.Form):
    """
    Formularz Kontaktowy
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input', 'id': 'contact_name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'contact_input', 'id': 'contact_email'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input', 'id': 'contact_subject'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'contact_input contact_textarea', 'id': 'contact_message', 'maxlength': '1000'}))


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Profile
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input', 'autofocus': 'autofocus'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'contact_input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'contact_input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'contact_input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all())
    product = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Product.objects.all())
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'contact_input'}))
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'contact_input contact_textarea', 'maxlength': '1000'}))
    stars = forms.ChoiceField(choices=STAR_CHOICES, widget=forms.RadioSelect(), required=True)

    class Meta:
        model = Reviews
        fields = ('user', 'product', 'title', 'text', 'stars')


class UpdateUser(forms.ModelForm):
    # username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'contact_input'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'contact_input'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'contact_input'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'contact_input'}))
    # password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'contact_input'}))
    # password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'contact_input'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
