from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .helpers import get_user_data
from django.contrib.auth.decorators import login_required

from .models import Portfolio, Certification, Education, Employment, About, Profilephoto
from .forms import PortfolioForm, CertificationForm, EducationForm, EmploymentForm, AboutForm, ProfilephotoForm

# render edit home page
def home(request):
    return render(request, 'home-page.html')

# render show portfolio page
def user_profile(request, username):
    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect('home')

    context = {
        'target_user': target_user,
        **data,  # Unpack the user-related data
    }
    return render(request, 'user-portfolio.html', context)


# render edit portfolio page
@login_required
def edit_user_profile(request, username):
    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect('home')

    context = {
        'target_user': target_user,
        **data,  # Unpack the user-related data
    }
    return render(request, 'edit-user-portfolio.html', context)


# Handle Create, Update and Delete for Portfolio
@login_required
def add_portfolio(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            messages.success(request, "Portfolio added successfully.")
            return redirect('edit_user_profile', username=request.user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Adding Portfolio: {error}")
    return redirect('edit_user_profile', username=request.user.username)


@login_required
def edit_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, "Portfolio updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Updating Portfolio: {error}")
        return redirect('edit_user_profile', username=request.user.username)

    return redirect('edit_user_profile', username=request.user.username)
	

@login_required
def delete_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
    if request.method == "POST":
        try:
            portfolio.delete()
            messages.success(request, "Portfolio deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the portfolio: {str(e)}")
        return redirect('edit_user_profile', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_profile', username=request.user.username)
    
# Handle Create, Update and Delete for Certification
@login_required
def add_certification(request):
    if request.method == "POST":
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = request.user
            certification.save()
            messages.success(request, "Certification added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Adding Certification: {error}")
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def edit_certification(request, id):
    certification = get_object_or_404(Certification, id=id, user=request.user)
    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Updating Certification: {error}")
        return redirect('edit_user_profile', username=request.user.username)
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def delete_certification(request, id):
    certification = get_object_or_404(Certification, id=id, user=request.user)
    if request.method == "POST":
        try:
            certification.delete()
            messages.success(request, "Certification deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the certification: {str(e)}")
        return redirect('edit_user_profile', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_profile', username=request.user.username)


# Handle Create, Update and Delete for Education
@login_required
def add_education(request):
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, "Education entry added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Adding Education: {error}")
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def edit_education(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education entry updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Updating Education: {error}")
        return redirect('edit_user_profile', username=request.user.username)
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def delete_education(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    if request.method == "POST":
        try:
            education.delete()
            messages.success(request, "Education entry deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the education entry: {str(e)}")
        return redirect('edit_user_profile', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_profile', username=request.user.username)


# Handle Create, Update and Delete for Employment
@login_required
def add_employment(request):
    if request.method == "POST":
        form = EmploymentForm(request.POST)
        if form.is_valid():
            employment = form.save(commit=False)
            employment.user = request.user
            employment.save()
            messages.success(request, "Employment entry added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Adding Employment: {error}")
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def edit_employment(request, id):
    employment = get_object_or_404(Employment, id=id, user=request.user)
    if request.method == "POST":
        form = EmploymentForm(request.POST, instance=employment)
        if form.is_valid():
            form.save()
            messages.success(request, "Employment entry updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Updating Employment: {error}")
        return redirect('edit_user_profile', username=request.user.username)
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def delete_employment(request, id):
    employment = get_object_or_404(Employment, id=id, user=request.user)
    if request.method == "POST":
        try:
            employment.delete()
            messages.success(request, "Employment entry deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the employment entry: {str(e)}")
        return redirect('edit_user_profile', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_profile', username=request.user.username)


# Handle Create, Update and Delete for About
@login_required
def save_about(request):
    about, created = About.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = AboutForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, "About section saved successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Saving About: {error}")
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def delete_about(request):
    about = get_object_or_404(About, user=request.user)
    if request.method == "POST":
        try:
            about.delete()
            messages.success(request, "About section deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the About section: {str(e)}")
    return redirect('edit_user_profile', username=request.user.username)

# Handle Create, Update and Delete for Profile Photo
@login_required
def save_profile_photo(request):
    try:
        profile_photo = Profilephoto.objects.get(user=request.user)
    except Profilephoto.DoesNotExist:
        profile_photo = Profilephoto(user=request.user)
    
    if request.method == "POST":
        form = ProfilephotoForm(request.POST, request.FILES, instance=profile_photo)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile photo saved successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Saving Profile Photo: {error}")
    return redirect('edit_user_profile', username=request.user.username)

@login_required
def delete_profile_photo(request):
    profile_photo = get_object_or_404(Profilephoto, user=request.user)
    if request.method == "POST":
        try:
            profile_photo.delete()
            messages.success(request, "Profile photo deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the profile photo: {str(e)}")
    return redirect('edit_user_profile', username=request.user.username)
