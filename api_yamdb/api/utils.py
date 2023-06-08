from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_ADDRESS


def send_confirmation_code(email, confirmation_code):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=EMAIL_ADDRESS,
        recipient_list=(email,),
        fail_silently=False,
    )
