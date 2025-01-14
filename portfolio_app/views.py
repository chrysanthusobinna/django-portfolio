from django.shortcuts import render
from .models import  About, Employment, Certification, Education, Portfolio, Contact
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
    return render(request, 'home-page.html')

def user_profile(request, username):
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "The user you are looking for does not exist.")
        # Redirect to the home page
        return redirect('home')

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
