from email.mime import image
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from users.models import User


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'image',
            'username',)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    image = forms.ImageField(required=False)
    username = forms.CharField()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2')
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    

class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField()
    
    password = forms.CharField()
    
    class Meta:
        model = User
        fields = ('username', 'password')