from django.core.mail import send_mail


def send_registration_email(email):
    subject = 'Регистрация успешна'
    message = 'Добро пожаловать! Вы успешно зарегистрировались.'
    from_email = 'your@example.com'  
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

