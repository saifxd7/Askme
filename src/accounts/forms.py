from django import forms
import json
import urllib
import urllib.request
from blog import settings
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)

from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    #email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            # 'email2',
            'password'
        ]
