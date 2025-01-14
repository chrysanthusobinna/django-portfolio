from django.shortcuts import render, get_object_or_404
from .models import  About, Employment, Certification, Education, Portfolio, Contact
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home-page.html')

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    # Get the related data for the user
    about = About.objects.filter(user=user).first()
    employment = Employment.objects.filter(user=user)
    certifications = Certification.objects.filter(user=user)
    education = Education.objects.filter(user=user)
    portfolios = Portfolio.objects.filter(user=user)
    contact = Contact.objects.filter(user=user).first()

    context = {
        'user': user,
        'about': about,
        'employment': employment,       
        'certifications': certifications,
        'education': education,
        'portfolios': portfolios,
        'contact': contact,
    }
    
    return render(request, 'user-portfolio.html', context)
