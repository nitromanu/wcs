__author__ = 'kurakar'

from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    """

    This is for validating the registration class and also for saving data into the database.
    The class Meta describes the model which we need to use.

    """
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)
    username = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    phone = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')

    def clean_username(self):
        """
        This method is for validating the username field.
        Prefix clean will taken automatically by django
        Here we raise validation errors if there are some errors.
        :return:username
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise forms.ValidationError('Email already registered')
        else:
            return username


class LoginForm(forms.Form):
    # This form class is for validating the login form
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
    school= forms.TimeField(required=True)

