from django.conf import settings
from django.core.mail import send_mail
from .views import *
from .models import *
from .apps import *

def send_email_to_client(Order):
    subject="YOUR ORDER HAS BEEN CONFORMED"
    message="thanks for shoping from KIYAN-OVERSEAS. your order will be dilivere soon !"
    from_email=settings.EMAIL_HOST_USER 
    recipient_list=[Order.email,settings.EMAIL_HOST_USER]
    send_mail(subject,message,from_email,recipient_list)
    
def send_user(Order):
    subject="ORDER CANCLED"
    message="Look into the admin panel and see any order or item is cancled by the user "
    from_email=settings.EMAIL_HOST_USER 
    recipient_list=[settings.EMAIL_HOST_USER]
    send_mail(subject,message,from_email,recipient_list)