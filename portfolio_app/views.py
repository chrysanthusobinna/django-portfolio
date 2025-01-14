from django.shortcuts import render, get_object_or_404
from .models import  About, Employment, Certification, Education, Portfolio, Contact
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home-page.html')

def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    
    # Get the related data for the user, or set to None if not found
    about = About.objects.filter(user=target_user).first() or None
    employment = Employment.objects.filter(user=target_user) or None
    certifications = Certification.objects.filter(user=target_user) or None
    education = Education.objects.filter(user=target_user) or None
    portfolios = Portfolio.objects.filter(user=target_user) or None
    contact = Contact.objects.filter(user=target_user).first() or None

    context = {
        'target_user': target_user,
        'about': about,
        'employment': employment,       
        'certifications': certifications,
        'education': education,
        'portfolios': portfolios,
        'contact': contact,
    }
    
    return render(request, 'user-portfolio.html', context)
