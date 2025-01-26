from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib import messages
from django.dispatch import receiver


@receiver(user_logged_in)
def custom_user_logged_in_message(request, user, **kwargs):
    first_name = user.first_name if user.first_name else user.email
    messages.success(request, f"Welcome , {first_name}!")


@receiver(user_signed_up)
def custom_user_signed_up_message(request, user, **kwargs):
    success_msg = "Registration successful!"
    first_name = user.first_name if user.first_name else user.email
    messages.success(request, f"{success_msg}!")
