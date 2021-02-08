from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
import json
import urllib
import urllib.request
from blog import settings


def login_view(request):

    # print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():

        #   ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')

        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        # ''' End reCAPTCHA validation '''

        if result['success']:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Login Successfully.')
            if next:
                return redirect(next)
            return redirect("/")

        else:
            messages.error(
                request, 'Invalid reCAPTCHA. Please try again.')

    return render(request, "form.html", {"form": form, "title": title})


def register_view(request):
    # print(request.user.is_authenticated())

    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():

        #   ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        # ''' End reCAPTCHA validation '''

        if result['success']:
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(
                username=user.username, password=password)
            messages.success(request, 'Register Successfully.')
            login(request, new_user)

            if next:
                return redirect(next)
            return redirect("/")

        else:
            messages.error(
                request, 'Invalid reCAPTCHA. Please try again.')

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successfully..')
    return redirect("/")
