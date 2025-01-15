from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .helpers import get_user_data
from django.contrib.auth.decorators import login_required

from .models import Portfolio, Certification, Education, Employment, About
from .forms import PortfolioForm, CertificationForm, EducationForm, EmploymentForm, AboutForm

def home(request):
    return render(request, 'home-page.html')


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



@login_required
def edit_user_profile(request, username):
    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect('home')

    if request.method == "POST":
        # Handle form submission for all models
        about_text = request.POST.get('about')
        if about_text:
            if data['about']:
                data['about'].about = about_text
                data['about'].save()
            else:
                About.objects.create(user=target_user, about=about_text)

        employment_ids = request.POST.getlist('employment_id')
        employment_employers = request.POST.getlist('employer_name')
        employment_titles = request.POST.getlist('job_title')
        employment_descriptions = request.POST.getlist('description_of_duties')
        employment_start_dates = request.POST.getlist('start_date')
        employment_end_dates = request.POST.getlist('end_date')

        for idx, emp_id in enumerate(employment_ids):
            if emp_id:  # Update existing employment
                employment = Employment.objects.get(id=emp_id)
                employment.employer_name = employment_employers[idx]
                employment.job_title = employment_titles[idx]
                employment.description_of_duties = employment_descriptions[idx]
                employment.start_date = employment_start_dates[idx]
                employment.end_date = employment_end_dates[idx]
                employment.save()
            else:  # Create new employment
                Employment.objects.create(
                    user=target_user,
                    employer_name=employment_employers[idx],
                    job_title=employment_titles[idx],
                    description_of_duties=employment_descriptions[idx],
                    start_date=employment_start_dates[idx],
                    end_date=employment_end_dates[idx],
                )

        # Repeat similar logic for Certifications, Education, Portfolios, and Contacts
        # Example for Certifications:
        certification_ids = request.POST.getlist('certification_id')
        certification_names = request.POST.getlist('certification_name')
        certification_issuers = request.POST.getlist('certification_issuer')
        certification_dates = request.POST.getlist('certification_date')

        for idx, cert_id in enumerate(certification_ids):
            if cert_id:  # Update existing certification
                certification = Certification.objects.get(id=cert_id)
                certification.name = certification_names[idx]
                certification.issuer = certification_issuers[idx]
                certification.date_issued = certification_dates[idx]
                certification.save()
            else:  # Create new certification
                Certification.objects.create(
                    user=target_user,
                    name=certification_names[idx],
                    issuer=certification_issuers[idx],
                    date_issued=certification_dates[idx],
                )

        # Repeat for Education, Portfolio, and Contact similarly

        messages.success(request, "Profile updated successfully!")
        return redirect('edit_user_portfolio', username=username)

    context = {
        'target_user': target_user,
        **data,  # Unpack user-related data
    }
    return render(request, 'edit-user-portfolio.html', context)

# Handle Create, Update and Delete for Portfolio
@login_required
def add_portfolio(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            messages.success(request, "Portfolio added successfully.")
            return redirect('edit_user_portfolio', username=request.user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Adding Portfolio: {error}")
    return redirect('edit_user_portfolio', username=request.user.username)


@login_required
def edit_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, "Portfolio updated successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error Updating Portfolio: {error}")
        return redirect('edit_user_portfolio', username=request.user.username)

    return redirect('edit_user_portfolio', username=request.user.username)
	

@login_required
def delete_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
    if request.method == "POST":
        try:
            portfolio.delete()
            messages.success(request, "Portfolio deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the portfolio: {str(e)}")
        return redirect('edit_user_portfolio', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_portfolio', username=request.user.username)
    
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
    return redirect('edit_user_portfolio', username=request.user.username)

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
        return redirect('edit_user_portfolio', username=request.user.username)
    return redirect('edit_user_portfolio', username=request.user.username)

@login_required
def delete_certification(request, id):
    certification = get_object_or_404(Certification, id=id, user=request.user)
    if request.method == "POST":
        try:
            certification.delete()
            messages.success(request, "Certification deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the certification: {str(e)}")
        return redirect('edit_user_portfolio', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_portfolio', username=request.user.username)


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
    return redirect('edit_user_portfolio', username=request.user.username)

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
        return redirect('edit_user_portfolio', username=request.user.username)
    return redirect('edit_user_portfolio', username=request.user.username)

@login_required
def delete_education(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    if request.method == "POST":
        try:
            education.delete()
            messages.success(request, "Education entry deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the education entry: {str(e)}")
        return redirect('edit_user_portfolio', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_portfolio', username=request.user.username)


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
    return redirect('edit_user_portfolio', username=request.user.username)

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
        return redirect('edit_user_portfolio', username=request.user.username)
    return redirect('edit_user_portfolio', username=request.user.username)

@login_required
def delete_employment(request, id):
    employment = get_object_or_404(Employment, id=id, user=request.user)
    if request.method == "POST":
        try:
            employment.delete()
            messages.success(request, "Employment entry deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the employment entry: {str(e)}")
        return redirect('edit_user_portfolio', username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('edit_user_portfolio', username=request.user.username)


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
    return redirect('edit_user_portfolio', username=request.user.username)

@login_required
def delete_about(request):
    about = get_object_or_404(About, user=request.user)
    if request.method == "POST":
        try:
            about.delete()
            messages.success(request, "About section deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the About section: {str(e)}")
    return redirect('edit_user_portfolio', username=request.user.username)