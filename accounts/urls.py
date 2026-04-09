
from django.urls import path

from . import views
from .gmail_api import send_gmail_api_email

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('send-gmail/', send_gmail_api_email, name='send_gmail_api_email'),
]
