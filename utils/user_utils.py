from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode


def generate_token_and_user_id_base64(user):
    token = default_token_generator.make_token(user)
    user_id_base64 = urlsafe_base64_encode(smart_bytes(user.id))
    return {'uib64': user_id_base64, 'token': token}


def email_verification_link_generator(user):
    relative_link = reverse('user:verify-email', kwargs=generate_token_and_user_id_base64(user))
    link = 'http://127.0.0.1:8000' + relative_link
    return f'Hi {user.username}! This link is for verifying your email: {link}'


def body_generator(user):
    return {
        'subject': 'Verify Your Email',
        'message': email_verification_link_generator(user)
    }


def send_email(user):
    user.email_user(**body_generator(user))
