from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.contrib import messages
import logging

from .helpers import get_user_data

from .models import (
    Contact,
    Portfolio,
    Certification,
    Education,
    Employment,
    About,
    Profilephoto,
    Template,
    UserTemplate,
    Skill,
)
from .forms import (
    ContactForm,
    PortfolioForm,
    CertificationForm,
    EducationForm,
    EmploymentForm,
    AboutForm,
    ProfilephotoForm,
    CVUploadForm,
)
from .utils import validate_image_file, send_contact_email
from .cv_parser import CVParser
from .gemini_cv_extractor import GeminiCVExtractor
from django.conf import settings

logger = logging.getLogger(__name__)


def home(request):
    templates = Template.objects.filter(is_active=True)
    return render(request, "home-page.html", {'templates': templates})


def template_preview(request, template_name):
    try:
        template = Template.objects.get(template_file=template_name, is_active=True)
    except Template.DoesNotExist:
        messages.error(request, "Template not found.")
        return redirect("home")

    fullname = 'Chrysanthus Obinna'
    initials = ''.join([part[0].upper() for part in fullname.split() if part])

    sample_data = {
        'user_fullname': fullname,
        'user_initials': initials,
        'profilephoto': None,
        'template_id': template.id,  
        'about': type('obj', (object,), {'about': 'Experienced software engineer and technology leader with over 10 years of expertise in full-stack development, cloud architecture, and team leadership. Passionate about building scalable solutions and mentoring the next generation of developers.'})(),
        'employment': [
            type('obj', (object,), {'employer_name': 'TechVision Solutions', 'job_title': 'Senior Software Engineer', 'description_of_duties': 'Led a team of 8 developers in designing and building enterprise-grade web applications using Django and React.', 'start_date': '2021-03-01', 'end_date': None})(),
            type('obj', (object,), {'employer_name': 'CloudFirst Technologies', 'job_title': 'Full-Stack Developer', 'description_of_duties': 'Developed and maintained cloud-native applications on AWS. Built RESTful APIs and responsive front-end interfaces.', 'start_date': '2018-06-15', 'end_date': '2021-02-28'})(),
            type('obj', (object,), {'employer_name': 'Digital Innovations Ltd', 'job_title': 'Junior Software Developer', 'description_of_duties': 'Contributed to the development of client-facing web applications using Python and JavaScript.', 'start_date': '2015-09-01', 'end_date': '2018-05-31'})(),
        ],
        'education': [
            type('obj', (object,), {'qualification': 'MSc Computer Science', 'institution_name': 'University of Lagos', 'start_date': '2013-09-01', 'end_date': '2015-07-15'})(),
            type('obj', (object,), {'qualification': 'BSc Information Technology', 'institution_name': 'Federal University of Technology, Owerri', 'start_date': '2009-09-01', 'end_date': '2013-06-30'})(),
        ],
        'certifications': [
            type('obj', (object,), {'name': 'AWS Certified Solutions Architect', 'issuer': 'Amazon Web Services', 'date_issued': '2023-05-10'})(),
            type('obj', (object,), {'name': 'Google Professional Cloud Developer', 'issuer': 'Google Cloud', 'date_issued': '2022-11-20'})(),
            type('obj', (object,), {'name': 'Django Developer Certification', 'issuer': 'Django Software Foundation', 'date_issued': '2021-08-15'})(),
        ],
        'portfolios': [
            type('obj', (object,), {'title': 'E-Commerce Platform', 'description': 'A full-featured online shopping platform built with Django and React.', 'link': '#', 'portfolio_photo': None})(),
            type('obj', (object,), {'title': 'Task Management App', 'description': 'A collaborative project management tool with real-time updates.', 'link': '#', 'portfolio_photo': None})(),
            type('obj', (object,), {'title': 'Health & Fitness Tracker', 'description': 'A mobile-responsive health tracking application.', 'link': '#', 'portfolio_photo': None})(),
        ],
        'contact': type('obj', (object,), {'phone_number': '+234 801 234 5678', 'email_address': 'chrysanthusobinna@gmail.com', 'linkedin': 'https://www.linkedin.com/in/chrysanthusobinna'})(),
    }

    return render(request, f"template-previews/{template_name}.html", sample_data)


@login_required
def select_template(request, template_id):
    template = get_object_or_404(Template, id=template_id, is_active=True)
    
    if request.method == 'POST':
        # Get or create UserTemplate for this user
        user_template, created = UserTemplate.objects.get_or_create(
            user=request.user,
            defaults={'template': template}
        )
        
        if not created:
            user_template.template = template
            user_template.save()
        
        messages.success(request, f"Template '{template.name}' has been selected for your portfolio!")
        return JsonResponse({'success': True, 'message': 'Template selected successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


# render show portfolio page and handle contact form
def user_profile(request, username):
    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect("home")

    # Get user's selected template
    try:
        user_template = UserTemplate.objects.get(user=target_user)
        template_name = user_template.template.template_file if user_template.template else 'minimalist'
    except UserTemplate.DoesNotExist:
        template_name = 'minimalist'  # default template

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
        "is_owner": request.user.is_authenticated and request.user.username == username,
        **data,  # Unpack the user-related data
    }
    return render(request, f"template-previews/{template_name}.html", context)


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


# Handle Delete All for Employment, Education, Certifications
@login_required
def delete_all_employment(request):
    if request.method == "POST":
        try:
            deleted_count, _ = Employment.objects.filter(user=request.user).delete()
            messages.success(request, f"All employment records deleted successfully ({deleted_count} removed).")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting all employment records: {e}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_all_education(request):
    if request.method == "POST":
        try:
            deleted_count, _ = Education.objects.filter(user=request.user).delete()
            messages.success(request, f"All education records deleted successfully ({deleted_count} removed).")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting all education records: {e}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_all_certifications(request):
    if request.method == "POST":
        try:
            deleted_count, _ = Certification.objects.filter(user=request.user).delete()
            messages.success(request, f"All certification records deleted successfully ({deleted_count} removed).")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting all certification records: {e}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_all_portfolio(request):
    if request.method == "POST":
        try:
            deleted_count, _ = Portfolio.objects.filter(user=request.user).delete()
            messages.success(request, f"All portfolio records deleted successfully ({deleted_count} removed).")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting all portfolio records: {e}")
    return redirect("edit_user_profile", username=request.user.username)


# Handle Save and Delete for Skills
@login_required
def save_skills(request):
    """Save skills from the tag/chip input (JSON array in hidden field)."""
    import json

    if request.method == "POST":
        raw = request.POST.get("skills_json", "[]")
        try:
            skills_list = json.loads(raw)
            if not isinstance(skills_list, list):
                skills_list = []
        except (json.JSONDecodeError, TypeError):
            # Fallback: treat as comma-separated
            skills_list = [s.strip() for s in raw.split(",") if s.strip()]

        # Sanitise: trim, enforce max-length, deduplicate, cap at 30
        seen = set()
        clean = []
        for s in skills_list:
            s = str(s).strip()[:40]
            if s and s.lower() not in seen:
                seen.add(s.lower())
                clean.append(s)
            if len(clean) >= 30:
                break

        skill_obj, _ = Skill.objects.get_or_create(user=request.user)
        skill_obj.skills = clean
        skill_obj.save()
        messages.success(request, "Skills saved successfully.")

    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_skills(request):
    """Delete all skills for the current user."""
    if request.method == "POST":
        try:
            skill_obj = Skill.objects.get(user=request.user)
            skill_obj.delete()
            messages.success(request, "Skills deleted successfully.")
        except Skill.DoesNotExist:
            messages.error(request, "No skills to delete.")
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
def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, "You have been logged out successfully.")
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


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


@login_required
def upload_cv(request):
    """Handle CV upload: extract text with pdfplumber, parse with Gemini,
    fall back to regex CVParser if Gemini fails, then save."""
    if request.method == "POST":
        form = CVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            cv_file = form.cleaned_data['cv_file']

            try:
                # --- 1. Extract raw text via pdfplumber ---
                try:
                    import pdfplumber
                except ImportError:
                    messages.error(
                        request,
                        "PDF processing library not installed. "
                        "Please contact administrator.",
                    )
                    return redirect(
                        "edit_user_profile",
                        username=request.user.username,
                    )

                try:
                    with pdfplumber.open(cv_file) as pdf:
                        cv_text = "\n".join(
                            page.extract_text() or ""
                            for page in pdf.pages
                        )
                except Exception as e:
                    logger.error("pdfplumber extraction failed: %s", e)
                    messages.error(
                        request,
                        "Could not read the PDF. Please ensure it is "
                        "a valid PDF with readable text.",
                    )
                    return redirect(
                        "edit_user_profile",
                        username=request.user.username,
                    )

                if not cv_text or not cv_text.strip():
                    messages.error(
                        request,
                        "The PDF appears to be empty or contains no "
                        "readable text.",
                    )
                    return redirect(
                        "edit_user_profile",
                        username=request.user.username,
                    )

                # --- 2. Parse with Gemini (primary) ---
                parsed_data = None
                try:
                    extractor = GeminiCVExtractor()
                    parsed_data = extractor.extract(cv_text)
                except ValueError as exc:
                    # GEMINI_API_KEY not configured
                    logger.warning("Gemini unavailable: %s", exc)
                except Exception as exc:
                    logger.error("Gemini extraction error: %s", exc)

                # --- 3. Fallback to regex parser ---
                if parsed_data is None:
                    logger.info("Falling back to regex CVParser")
                    cv_file.seek(0)  # rewind for re-read
                    parser = CVParser()
                    parsed_data = parser.parse_cv(cv_file)

                if not parsed_data:
                    messages.error(
                        request,
                        "Could not extract data from the CV. "
                        "Please ensure it's a valid PDF with "
                        "readable text.",
                    )
                    return redirect(
                        "edit_user_profile",
                        username=request.user.username,
                    )

                # --- 4. Save extracted data ---
                _save_parsed_cv_data(request, parsed_data)

                messages.success(
                    request,
                    "CV data has been successfully extracted "
                    "and added to your portfolio!",
                )

            except Exception as e:
                messages.error(request, f"Error processing CV: {str(e)}")
                logger.error("CV processing error: %s", e, exc_info=True)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"CV Upload Error: {error}")

    return redirect("edit_user_profile", username=request.user.username)


def _save_parsed_cv_data(request, parsed_data):
    """
    Save / upsert parsed CV data into Django models.

    De-duplication rules:
    - Contact & About  → get_or_create then update.
    - Employment       → unique on (user, employer_name, job_title, start_date).
    - Education        → unique on (user, institution_name, qualification, start_date).
    - Certification    → unique on (user, name, issuer).
    - Portfolio        → unique on (user, title).
    """
    user = request.user

    # --- Contact ---
    contact_raw = parsed_data.get("contact") or {}
    # Support both key styles  (email_address / email, phone_number / phone)
    email = (
        contact_raw.get("email_address")
        or contact_raw.get("email")
    )
    phone = (
        contact_raw.get("phone_number")
        or contact_raw.get("phone")
    )
    linkedin = contact_raw.get("linkedin")

    if email or phone or linkedin:
        contact, _ = Contact.objects.get_or_create(user=user)
        if email:
            contact.email_address = email
        if phone:
            contact.phone_number = phone
        if linkedin:
            contact.linkedin = linkedin
        contact.save()

    # --- About ---
    about_text = parsed_data.get("about")
    if about_text and str(about_text).strip():
        about, _ = About.objects.get_or_create(user=user)
        about.about = str(about_text).strip()
        about.save()

    # --- Employment (upsert) ---
    for emp in parsed_data.get("employment") or []:
        if not emp.get("employer_name") and not emp.get("job_title"):
            continue
        # start_date is NOT NULL in DB — use fallback if missing
        start_date = emp.get("start_date") or "2000-01-01"
        lookup = {
            "user": user,
            "employer_name": emp.get("employer_name") or "",
            "job_title": emp.get("job_title") or "",
            "start_date": start_date,
        }
        defaults = {
            "description_of_duties": emp.get("description_of_duties") or "",
            "end_date": emp.get("end_date"),
        }
        Employment.objects.update_or_create(defaults=defaults, **lookup)

    # --- Education (upsert) ---
    for edu in parsed_data.get("education") or []:
        if not edu.get("institution_name"):
            continue
        # start_date is NOT NULL in DB — use fallback if missing
        start_date = edu.get("start_date") or "2000-01-01"
        lookup = {
            "user": user,
            "institution_name": edu.get("institution_name") or "",
            "qualification": edu.get("qualification") or "",
            "start_date": start_date,
        }
        defaults = {
            "end_date": edu.get("end_date"),
        }
        Education.objects.update_or_create(defaults=defaults, **lookup)

    # --- Certifications (upsert) ---
    for cert in parsed_data.get("certifications") or []:
        if not cert.get("name"):
            continue
        # date_issued is NOT NULL in DB — use fallback if missing
        date_issued = cert.get("date_issued") or "2000-01-01"
        lookup = {
            "user": user,
            "name": cert.get("name") or "",
            "issuer": cert.get("issuer") or "",
        }
        defaults = {
            "date_issued": date_issued,
        }
        Certification.objects.update_or_create(defaults=defaults, **lookup)

    # --- Projects / Portfolio (upsert) ---
    for proj in parsed_data.get("projects") or []:
        if not proj.get("title"):
            continue
        lookup = {
            "user": user,
            "title": proj.get("title") or "",
        }
        defaults = {
            "description": proj.get("description") or "",
            "link": proj.get("link") or "",
        }
        Portfolio.objects.update_or_create(defaults=defaults, **lookup)

    # --- Skills (merge with existing) ---
    skills_raw = parsed_data.get("skills") or []
    if skills_raw:
        if isinstance(skills_raw, str):
            skills_raw = [s.strip() for s in skills_raw.split(",") if s.strip()]
        skill_obj, _ = Skill.objects.get_or_create(user=user)
        existing = set(s.lower() for s in skill_obj.get_skills_list())
        merged = list(skill_obj.get_skills_list())
        for s in skills_raw:
            s = str(s).strip()[:40]
            if s and s.lower() not in existing and len(merged) < 30:
                existing.add(s.lower())
                merged.append(s)
        skill_obj.skills = merged
        skill_obj.save()
