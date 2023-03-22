from club.models import User, Club
from django import forms
from django.contrib.auth import authenticate
import re


class RegisterForm(forms.ModelForm):
    # required fields for register
    email = forms.EmailField(help_text="Please enter the email.")
    username = forms.CharField(help_text="Please enter the username.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter the password.")
    birthday = forms.DateField(input_formats=['%Y-%m-%d'], help_text="Please enter the birthday.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birthday')

    # add restriction to username field
    def clean_username(self):
        username = self.cleaned_data['username']
        # if the length of username is less than 2, return error
        if len(username) < 2:
            raise forms.ValidationError("Username is too short.")
        return username

    # add restriction to password field
    def clean_password(self):
        password = self.cleaned_data['password']
        # using regex, Require passwords to be at least 8 characters long and contain at least one number and one letter
        pattern = r'^(?=.*[A-Za-z])(?=.*\d).+$'
        if not (len(password) >= 8 and re.match(pattern, password)):
            raise forms.ValidationError("The password should be at least 8 characters long and contain at least one letter and one number.")
        return password


class LoginForm(forms.ModelForm):
    # required fields for login
    email = forms.EmailField(help_text="Please enter the email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter the password.")

    def clean(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        # add authentication here, if the user is not authenticated, return error
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError('Email or password is not correct！')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('email', 'password')


class CreateClubForm(forms.ModelForm):
    # Predefined types of clubs
    options = (
        ("Sport", "Sport"),
        ("Arts & Culture", "Arts & Culture"),
        ("Academic", "Academic"),
        ("Social & Service", "Social & Service"),
        ("Political", "Political"),
        ("Animals", "Animals"),
    )

    # required fields for create club
    name = forms.CharField(max_length=20, help_text="Please enter the name of the club.")
    type = forms.ChoiceField(choices=options, help_text="Please select the type of the page.")
    location = forms.CharField(max_length=20, help_text="Please enter the city of the page.")
    description = forms.CharField(widget=forms.Textarea, max_length=200, help_text="Please enter the description of the club.")

    # add restriction to name field
    def clean_name(self):
        name = self.cleaned_data['name']
        # if the length of name is less than 2, return error
        if len(name) < 2:
            raise forms.ValidationError("Name is too short.")
        return name

    # add restriction to type field
    def clean_type(self):
        type = self.cleaned_data['type']
        # If the selected type is not within the predefined range, return error
        if type not in dict(self.options):
            raise forms.ValidationError("Type is invalid.")
        return type

    class Meta:
        model = Club
        fields = ('name', 'type', 'location', 'description')