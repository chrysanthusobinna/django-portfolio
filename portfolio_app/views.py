from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .helpers import get_user_data
from django.contrib.auth.decorators import login_required

from .models import (
    Contact,
    Portfolio,
    Certification,
    Education,
    Employment,
    About,
    Profilephoto,
)
from .forms import (
    ContactForm,
    PortfolioForm,
    CertificationForm,
    EducationForm,
    EmploymentForm,
    AboutForm,
    ProfilephotoForm,
)
from .utils import validate_image_file, send_contact_email
from django.conf import settings


def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        full_message = f"Name: {name}\nEmail: {email}\n\n{message}"

        is_valid, error_message = send_contact_email(
            subject, full_message, [settings.SITE_CONTACT_EMAIL_ADDRESS]
        )
        if is_valid:
            messages.success(
                request, "Your message has been sent successfully!")
        else:
            messages.error(request, error_message)
        return redirect("home")

    return render(request, "home-page.html")


# render show portfolio page and handle contact form
def user_profile(request, username):
    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = f"{name} From your portfolio contact form"
        message = request.POST.get("message")
        full_message = f"Name: {name}\nEmail: {email}\n\n{message}"

        is_valid, error_message = send_contact_email(
            subject, full_message, [target_user.email]
        )
        if is_valid:
            messages.success(
                request, "Your message has been sent successfully!")
        else:
            messages.error(request, error_message)
        return redirect("user_profile", username=target_user.username)

    context = {
        "target_user": target_user,
        **data,  # Unpack the user-related data
    }
    return render(request, "user-portfolio.html", context)


# render edit portfolio page
@login_required
def edit_user_profile(request, username):
    if request.user.username != username:
        messages.error(request, "You cannot update another user's profile.")
        return redirect("home")

    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect("home")

    context = {
        "target_user": target_user,
        **data,  # Unpack the user-related data
    }
    return render(request, "edit-user-portfolio.html", context)


# Handle Create, Update and Delete for Portfolio
@login_required
def add_portfolio(request):
    error_msg = "Error Adding Portfolio: "
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)

        # Validate the uploaded image file
        is_valid, error_message = validate_image_file(
            request, "portfolio_photo", "Portfolio Photo"
        )
        if not is_valid:
            messages.error(request, error_message)
            return redirect("edit_user_profile", username=request.user.username)  # noqa

        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            messages.success(request, "Portfolio added successfully.")
            return redirect("edit_user_profile", username=request.user.username)  # noqa
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def edit_portfolio(request, id):
    error_msg = "Error Updating Portfolio: "
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)

    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)

        # Validate the uploaded image file
        is_valid, error_message = validate_image_file(
            request, "portfolio_photo", "Portfolio Photo"
        )
        if not is_valid:
            messages.error(request, error_message)
            return redirect("edit_user_profile", username=request.user.username)  # noqa

        if form.is_valid():
            form.save()
            messages.success(request, "Portfolio updated successfully.")
            return redirect("edit_user_profile", username=request.user.username)  # noqa
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
    if request.method == "POST":
        try:
            portfolio.delete()
            messages.success(request, "Portfolio deleted successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while trying to delete the portfolio: {str(e)}")  # noqa
        return redirect("edit_user_profile", username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect("edit_user_profile", username=request.user.username)


# Handle Create, Update and Delete for Certification
@login_required
def add_certification(request):
    error_msg = "Error Adding Certification: "
    if request.method == "POST":
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = request.user
            certification.save()
            messages.success(request, "Certification added successfully.")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def edit_certification(request, id):
    error_msg = "Error Updating Certification: "
    certification = get_object_or_404(Certification, id=id, user=request.user)

    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, "Certification updated successfully.")
            return redirect("edit_user_profile", username=request.user.username)  # noqa
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_certification(request, id):
    certification = get_object_or_404(Certification, id=id, user=request.user)
    error_msg = (
        "An error occurred while trying "
        "to delete the certification: "
    )
    if request.method == "POST":
        try:
            certification.delete()
            messages.success(request, "Certification deleted successfully.")
        except Exception as e:
            messages.error(request, f"{error_msg}{e}")
    else:
        messages.error(request, "Invalid request method.")
    return redirect("edit_user_profile", username=request.user.username)


# Handle Create, Update and Delete for Education
@login_required
def add_education(request):
    error_msg = "Error Adding Education: "
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, "Education entry added successfully.")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def edit_education(request, id):
    error_msg = "Error Updating Education: "
    education = get_object_or_404(Education, id=id, user=request.user)

    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education entry updated successfully.")
            return redirect("edit_user_profile", username=request.user.username)  # noqa
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_education(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    error_msg = (
        "An error occurred while trying to delete "
        "the education entry: "
    )
    if request.method == "POST":
        try:
            education.delete()
            messages.success(request, "Education entry deleted successfully.")
        except Exception as e:
            messages.error(request, f"{error_msg}{e}")
        return redirect("edit_user_profile", username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect("edit_user_profile", username=request.user.username)


# Handle Create, Update and Delete for Employment
@login_required
def add_employment(request):
    error_msg = "Error Adding Employment: "
    if request.method == "POST":
        form = EmploymentForm(request.POST)
        if form.is_valid():
            employment = form.save(commit=False)
            employment.user = request.user
            employment.save()
            messages.success(request, "Employment entry added successfully.")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def edit_employment(request, id):
    error_msg = "Error Updating Employment: "
    employment = get_object_or_404(Employment, id=id, user=request.user)

    if request.method == "POST":
        form = EmploymentForm(request.POST, instance=employment)
        if form.is_valid():
            form.save()
            messages.success(request, "Employment entry updated successfully.")
            return redirect("edit_user_profile", username=request.user.username)  # noqa
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_employment(request, id):
    error_msg = (
        "An error occurred while trying to "
        "delete the employment entry: "
    )
    employment = get_object_or_404(Employment, id=id, user=request.user)
    if request.method == "POST":
        try:
            employment.delete()
            messages.success(request, "Employment entry deleted successfully.")
        except Exception as e:
            messages.error(request, f"{error_msg}{e}")
        return redirect("edit_user_profile", username=request.user.username)
    else:
        messages.error(request, "Invalid request method.")
        return redirect("edit_user_profile", username=request.user.username)


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
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_about(request):
    error_msg = (
        "An error occurred while trying to "
        "delete the About section:  "
    )
    about = get_object_or_404(About, user=request.user)
    if request.method == "POST":
        try:
            about.delete()
            messages.success(request, "About section deleted successfully.")
        except Exception as e:
            messages.error(request, f"{error_msg}{e}")
    return redirect("edit_user_profile", username=request.user.username)


# Handle Create, Update, and Delete for Profile Photo
@login_required
def save_profile_photo(request):
    error_msg = (
        "Error Saving Profile Photo: "
    )
    try:
        profile_photo = Profilephoto.objects.get(user=request.user)
    except Profilephoto.DoesNotExist:
        profile_photo = Profilephoto(user=request.user)

    if request.method == "POST":
        form = ProfilephotoForm(
            request.POST, request.FILES, instance=profile_photo
            )

        # Validate the uploaded image file
        is_valid, error_message = validate_image_file(
            request, "profile_photo", "Profile Photo"
        )
        if not is_valid:
            messages.error(request, error_message)
            return redirect(
                "edit_user_profile", username=request.user.username
                )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile photo saved successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error_msg}{error}")  # noqa
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_profile_photo(request):
    error_msg = (
        "An error occurred while trying to "
        "delete the profile photo: "
    )
    profile_photo = get_object_or_404(Profilephoto, user=request.user)
    if request.method == "POST":
        try:
            profile_photo.delete()
            messages.success(request, "Profile photo deleted successfully.")
        except Exception as e:
            messages.error(request, f"{error_msg}{e}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def contact_update(request):
    error_msg = "Error Saving Contact: "
    try:
        contact = Contact.objects.get(user=request.user)
    except Contact.DoesNotExist:
        contact = None

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, "Contact updated successfully.")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def contact_delete(request):
    try:
        contact = Contact.objects.filter(user=request.user).first()
        if request.method == "POST":
            if contact:
                contact.delete()
                messages.success(request, "Contact deleted successfully.")
            else:
                messages.error(request, "Contact not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    return redirect("edit_user_profile", username=request.user.username)
