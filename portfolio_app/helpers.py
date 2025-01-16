from .models import Profilephoto, About, Employment, Certification, Education, Portfolio, Contact
from django.contrib.auth.models import User

def get_user_data(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None, None

    data = {
        'profilephoto': Profilephoto.objects.filter(user=user).first() or None,
        'about': About.objects.filter(user=user).first() or None,
        'employment': Employment.objects.filter(user=user) or None,
        'certifications': Certification.objects.filter(user=user) or None,
        'education': Education.objects.filter(user=user) or None,
        'portfolios': Portfolio.objects.filter(user=user) or None,
        'contact': Contact.objects.filter(user=user).first() or None,
    }
    return user, data
