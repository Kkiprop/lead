from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import EmailForm, InvestorSearchForm
from .gmail_api import GmailIntegrationError, get_gmail_service_for_user
from .lead_directory import search_investors


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    query = ''
    results = []
    selected_ids = []
    has_google_gmail = True
    gmail_status_message = ''
    search_form = InvestorSearchForm(request.GET or None)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        results = search_investors(query)

    if has_google_gmail:
        try:
            get_gmail_service_for_user(request.user)
        except GmailIntegrationError as exc:
            has_google_gmail = False
            gmail_status_message = str(exc)

    selected_contacts = [lead for lead in results if lead['id'] in selected_ids]
    context = {
        'search_form': search_form,
        'query': query,
        'results': results,
        'result_count': len(results),
        'selected_ids': selected_ids,
        'selected_contacts': selected_contacts,
        'selected_count': len(selected_contacts),
        'has_google_gmail': has_google_gmail,
        'gmail_status_message': gmail_status_message,
    }

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results_html = render_to_string('partials/dashboard_results.html', context, request=request)
        return JsonResponse(
            {
                'query': query,
                'result_count': len(results),
                'results_html': results_html,
            }
        )

    return render(request, 'dashboard.html', context)


@login_required
def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False,
            )
            return render(request, 'email_sent.html', {'to_email': to_email})
    else:
        form = EmailForm()
    return render(request, 'send_email.html', {'form': form})
