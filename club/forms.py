from django.contrib.auth.models import User
from club.models import UserProfile, Club
from django import forms
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class searchClubForm(forms.ModelForm):
    location = forms.CharField()
    # type = forms.CharField()
    class Meta:
        model = Club
        exclude = ()