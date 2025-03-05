from django.core.mail import send_mail
from django.conf import settings
import random
import string

def send_otp_email(email, name, otp_code):
    subject = 'Your OTP for Account Registration'
    message = f'''
    Hello {name},
    
    Your OTP for account registration is: {otp_code}
    
    This OTP will expire in 10 minutes.
    
    Thanks,
    Your App Team
    '''
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)