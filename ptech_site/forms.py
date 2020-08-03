from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    username = forms.CharField(max_length=30, help_text='Required')
    print("at forms ", username, email)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='username' ,help_text='Required')
    def clean_name(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('You have to type in a username.')
        return username

class UpdateProfileForm(forms.Form):
    print("forms", forms)
    title = forms.CharField(max_length=30, required=False)
    AboutMe = forms.CharField(max_length=230, required=False)
    Mobile = forms.CharField(max_length=230, required=False)
    password1= forms.PasswordInput()
    password2= forms.PasswordInput()
    print("at forms ", title, AboutMe)
    class Meta:
        model = User
        fields = ('title', 'AboutMe', 'Mobile', 'old_password', 'password1', 'password2')
