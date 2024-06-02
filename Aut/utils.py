from django.core.mail import send_mail
from django.conf import settings

def send_password_email(email, text):
    subject = 'Сброс пароля'
    message = text
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)