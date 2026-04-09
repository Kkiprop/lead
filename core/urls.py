"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.views.generic import TemplateView
from accounts.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', home_view, name='home'),
    path('welcome-email/', TemplateView.as_view(template_name='welcome_email.html'), name='welcome_email'),
    path('send-email/', TemplateView.as_view(template_name='send_email.html'), name='send_email'),
    path('email-sent/', TemplateView.as_view(template_name='email_sent.html'), name='email_sent'),
    path('base/', TemplateView.as_view(template_name='base.html'), name='base'),    
]
