from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(email, petition_title, answer):
    subject = 'Ответ на вашу петицию'
    message = f'Здравствуйте!\n\nПредставители власти ответили на вашу петицию "{petition_title}". \nОтвет: {answer}'
    sender_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, sender_email, recipient_list)
