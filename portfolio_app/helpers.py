from django.contrib.auth.models import User

from .models import (
    Profilephoto,
    About,
    Employment,
    Certification,
    Education,
    Portfolio,
    ContactMethod,
    Skill,
)

from django.contrib.auth.models import User


def get_user_data(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None, None

    # Concatenate first name and last name
    # if they exist, else use email address
    user_fullname = ""
    if user.first_name:
        user_fullname += user.first_name
    if user.last_name:
        user_fullname += " " + user.last_name
    user_fullname = user_fullname.strip() or user.email

    # Compute initials from first/last name, fallback to first 2 chars of email
    initials = ""
    if user.first_name:
        initials += user.first_name[0].upper()
    if user.last_name:
        initials += user.last_name[0].upper()
    if not initials:
        initials = user.email[:2].upper()

    data = {
        'profilephoto': Profilephoto.objects.filter(user=user).first() or None,
        'about': About.objects.filter(user=user).first() or None,
        'employment': Employment.objects.filter(user=user) or None,
        'certifications': Certification.objects.filter(user=user) or None,
        'education': Education.objects.filter(user=user) or None,
        'portfolios': Portfolio.objects.filter(user=user) or None,
        'contact_methods': ContactMethod.objects.filter(user=user),
        'skill': Skill.objects.filter(user=user).first() or None,
        'user_fullname': user_fullname,
        'user_initials': initials,
    }
    return user, data
