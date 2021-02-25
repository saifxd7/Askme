from .models import CustomUser
from django import forms
import json
import urllib
import urllib.request
from blog import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
# for reset,change pass
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, SetPasswordForm

from django.core.exceptions import ValidationError

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'autocomplete': 'off', 'data-toggle': 'password'}))

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
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Email address')
    #email2 = forms.EmailField(label='Confirm Email')

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'data-toggle': 'password'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            # 'email2',
            'password'
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'bio', 'location')


class PwdChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='Old Password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))
