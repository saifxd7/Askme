# Create your views here.
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


from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token


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
            # user = ASCIIUsernameValidator()
            password = form.cleaned_data.get('password')
            user.set_password(password)

            # current_site = get_current_site(request)
            # mail_subject = 'Activate your account.'
            # message = render_to_string('accounts/acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email]
            # )
            # email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            user.save()
            new_user = authenticate(username=user.username, password=password)
            messages.success(request, 'Register Successfully.')
            login(request, new_user)

            if next:
                return redirect(next)
            return redirect("/")

        else:
            messages.error(
                request, 'Invalid reCAPTCHA. Please try again.')

    else:
        form = UserRegisterForm()

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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')
