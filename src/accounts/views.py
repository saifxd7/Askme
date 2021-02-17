from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
import json
import urllib
import urllib.request
from blog import settings

from Qpost.models import *


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


# Profile
def profile(request):
    quests = Question.objects.filter(user=request.user).order_by('-id')
    answers = Answer.objects.filter(user=request.user).order_by('-id')
    comments = Comment.objects.filter(user=request.user).order_by('-id')
    upvotes = UpVote.objects.filter(user=request.user).order_by('-id')
    downvotes = DownVote.objects.filter(user=request.user).order_by('-id')
    if request.method == 'POST':
        profileForm = ProfileForm(request.POST, instance=request.user)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, 'Profile has been updated.')
    form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'quests': quests,
        'answers': answers,
        'comments': comments,
        'upvotes': upvotes,
        'downvotes': downvotes,
    })
