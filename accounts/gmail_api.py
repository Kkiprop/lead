import base64
import os
from email.mime.text import MIMEText

from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .forms import EmailForm


class GmailIntegrationError(Exception):
    pass


def get_safe_back_to(request, back_to_param):
    if back_to_param and url_has_allowed_host_and_scheme(
        back_to_param,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return back_to_param
    return ''


def get_gmail_service_for_user(user):
    try:
        social = SocialAccount.objects.get(user=user, provider='google')
    except SocialAccount.DoesNotExist as exc:
        raise GmailIntegrationError('No Google social account found. Please sign in with Google first.') from exc

    try:
        token = SocialToken.objects.get(account=social, account__user=user)
    except SocialToken.DoesNotExist as exc:
        raise GmailIntegrationError('No token stored for your Google account. Please re-authenticate.') from exc

    client_id = os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID', '')
    client_secret = os.getenv('SOCIAL_AUTH_GOOGLE_SECRET', '')
    if not client_id or not client_secret:
        raise GmailIntegrationError('Google OAuth credentials are not configured for Gmail sending.')

    credentials = Credentials(
        token=token.token,
        refresh_token=token.token_secret or None,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=['https://www.googleapis.com/auth/gmail.send'],
    )
    return build('gmail', 'v1', credentials=credentials)


def send_gmail_message(user, recipients, subject, message):
    recipient_list = [recipient.strip() for recipient in recipients if recipient and recipient.strip()]
    if not recipient_list:
        raise GmailIntegrationError('Select at least one recipient before sending email.')

    service = get_gmail_service_for_user(user)
    mime_message = MIMEText(message)
    mime_message['to'] = user.email or recipient_list[0]
    mime_message['bcc'] = ', '.join(recipient_list)
    mime_message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw_message}).execute()


@login_required
def send_gmail_api_email(request):
    debug_info = None
    initial_data = {}

    recipients_param = request.GET.get('recipients', '').strip()
    subject_param = request.GET.get('subject', '').strip()
    message_param = request.GET.get('message', '').strip()
    back_to_param = request.GET.get('back_to', '').strip()
    back_to_url = get_safe_back_to(request, back_to_param)
    google_reauth_next = request.get_full_path()
    if recipients_param:
        initial_data['to_email'] = recipients_param.replace(';', ', ')
    if subject_param:
        initial_data['subject'] = subject_param
    if message_param:
        initial_data['message'] = message_param

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipients = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_gmail_message(request.user, recipients, subject, message)
                request.session['email_sent_to'] = ', '.join(recipients)
                request.session.modified = True
                return HttpResponseRedirect(request.get_full_path())
            except Exception as exc:
                debug_info = f'Exception: {exc}'
                return render(
                    request,
                    'send_gmail.html',
                    {
                        'form': form,
                        'error': str(exc),
                        'debug_info': debug_info,
                        'back_to': back_to_url,
                        'google_reauth_next': google_reauth_next,
                    },
                )
    else:
        form = EmailForm(initial=initial_data)

    email_sent_to = None
    if request.method == 'GET' and 'email_sent_to' in request.session:
        email_sent_to = request.session['email_sent_to']
        del request.session['email_sent_to']
        request.session.modified = True
    return render(
        request,
        'send_gmail.html',
        {
            'form': form,
            'email_sent_to': email_sent_to,
            'debug_info': debug_info,
            'back_to': back_to_url,
            'google_reauth_next': google_reauth_next,
        },
    )
