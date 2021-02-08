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
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

# views import
from accounts import views as account_views

urlpatterns = [
    path('', include("Qpost.urls")),
    # path('blog/', include("boards.urls", namespace="blog-app")),
    path('admin/', admin.site.urls),
    # zpath('profile/', account_views.profile, name='profile'),
    path('register/', account_views.register_view, name='register'),
    # path('activate/<uidb64>/<token>/', account_views.activate, name='activate'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),


    # path('reset/', auth_views.Password_reset.as_view()),
    # path('reset/done/', auth_views.Password_reset_done.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
