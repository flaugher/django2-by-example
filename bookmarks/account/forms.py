from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    """Form for user to log in."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    """Form for user to edit their user information."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    """Form for user to edit their profile information."""
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

class UserRegistrationForm(forms.ModelForm):
    """Form for user to register an account."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """Check that passwords match.

        This is based on the Django UserCreationForm.  See t.ly/8LpX2

        Note that you can provide a clean_FIELDNAME for any form field.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
