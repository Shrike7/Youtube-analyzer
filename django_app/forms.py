from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_json_file_extension(value):
    if not value.name.endswith('.json'):
        raise ValidationError('Only JSON files are allowed.')


class JSONUploadForm(forms.Form):
    json_file = forms.FileField(
        label='Upload a JSON file',
        validators=[validate_json_file_extension]
    )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)


