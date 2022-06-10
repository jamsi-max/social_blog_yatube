# core/views.py
from django.shortcuts import render

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')


def server_error(request):
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'core/403.html', status=403)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def registrarion_send_mail(mail, username):
    subject = 'Спасибо за регистрацию на Yatube'
    from_email = 'yarube@yatube.com'
    to = mail
    html_message = render_to_string(
        'mail/email_template.html', context={'username': username})
    msg = EmailMessage(subject, html_message, from_email, [to])
    msg.content_subtype = 'html'
    msg.send()