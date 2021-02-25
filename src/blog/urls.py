"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

# forms
from accounts.forms import PwdResetForm, PwdChangeForm, PwdResetConfirmForm

# views import
from accounts import views as account_views

urlpatterns = [
    path('', include("Qpost.urls")),
    # path('blog/', include("boards.urls", namespace="blog-app")),
    path('admin/', admin.site.urls),
    path('profile/', account_views.profile, name='profile'),
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html",
                                                                 form_class=PwdResetForm), name='pwdreset'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form.html",
                                                                   form_class=PwdChangeForm), name='pwdforgot'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html', form_class=PwdResetConfirmForm), name="pwdresetconfirm"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('activate/<slug:uidb64>/<slug:token>)/',
         account_views.activate, name='activate'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
