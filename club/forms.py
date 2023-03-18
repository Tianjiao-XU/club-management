from club.models import User, Club
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birthday')


class searchClubForm(forms.ModelForm):
    location = forms.CharField()
    # type = forms.CharField()

    class Meta:
        model = Club
        exclude = ()