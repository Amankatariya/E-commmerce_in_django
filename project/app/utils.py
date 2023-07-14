from django.conf import settings
from .views import *
from .models import *
from .apps import *
from .templates import *
from django.core.mail import send_mail


def send_email_to_client(order):
    subject = "YOUR ORDER HAS BEEN CONFIRMED"
    message = "Thanks for shopping from KIYAN-OVERSEAS. Your order will be delivered soon!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [order.email, settings.EMAIL_HOST_USER]
    send_mail(subject, message, from_email, recipient_list)

def send_email_now():
    subject = "ORDER CANCELLED"
    message = "This order has been cancelled. Check it out now."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, from_email, recipient_list)

