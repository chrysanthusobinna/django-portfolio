from django.shortcuts import render, get_object_or_404
from .models import  About, Employment, Certification, Education, Portfolio, Contact
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home-page.html')

def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    
    # Get the related data for the user
    about = About.objects.filter(user=target_user).first()
    employment = Employment.objects.filter(user=target_user)
    certifications = Certification.objects.filter(user=target_user)
    education = Education.objects.filter(user=target_user)
    portfolios = Portfolio.objects.filter(user=target_user)
    contact = Contact.objects.filter(user=target_user).first()

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
