from club.models import User, Club
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),help_text="Please enter the password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'birthday')


class LoginForm(forms.ModelForm):
    email = forms.EmailField(help_text="Please enter the email.")
    password = forms.CharField(widget=forms.PasswordInput(),help_text="Please enter the password.")

    class Meta:
        model = User
        fields = ('email', 'password')

# class searchClubForm(forms.ModelForm):
#     location = forms.CharField(max_length=100)
#     # type = forms.CharField()
#
#     class Meta:
#         model = Club
#         fields = ('name','description','type','location','likes','dislikes')


class CreateClubForm(forms.ModelForm):
    options = (
        ("Sport", "Sport"),
        ("Arts & Culture", "Arts & Culture"),
        ("Academic", "Academic"),
        ("Social & Service", "Social & Service"),
        ("Political", "Political"),
        ("Religious", "Religious"),
        ("Ethnic", "Ethnic"),
        ("Animals", "Animals"),
    )

    name = forms.CharField(max_length=20, help_text="Please enter the name of the club.")
    type = forms.ChoiceField(choices=options, help_text="Please select the type of the page.")
    location = forms.CharField(max_length=20, help_text="Please enter the city of the page.")
    description = forms.CharField(widget=forms.Textarea, max_length=200, help_text="Please enter the description of the club.")

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError("Name is too short.")
        return name

    def clean_type(self):
        type = self.cleaned_data['type']
        if type not in dict(self.options):
            raise forms.ValidationError("Type is invalid.")
        return type

    class Meta:
        model = Club
        fields = ('name', 'type', 'location', 'description')