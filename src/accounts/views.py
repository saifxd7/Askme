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

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# for activate user
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse

User = get_user_model()


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
            user.email = form.cleaned_data['email']
            password = form.cleaned_data.get('password')
            try:
                validate_password(password, user)
            except ValidationError as e:
                # to be displayed with the field's errors
                form.add_error('password', e)
                return render(request, 'form.html', {'form': form, 'title': title})
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')

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


@login_required
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/activation_invalid.html')
