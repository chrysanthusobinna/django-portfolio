from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging

from .helpers import get_user_data

from .models import (
    ContactMethod,
    Portfolio,
    Certification,
    Education,
    Employment,
    About,
    Profilephoto,
    Template,
    UserTemplate,
    Skill,
    UserProfile,
)
from .forms import (
    ContactMethodForm,
    PortfolioForm,
    CertificationForm,
    EducationForm,
    EmploymentForm,
    AboutForm,
    ProfilephotoForm,
    CVUploadForm,
    AccountSettingsForm,
)
from .utils import validate_image_file, send_contact_email
from .cv_parser import CVParser
from .vertex_ai_cv_extractor import VertexAICVExtractor
from django.conf import settings

logger = logging.getLogger(__name__)

def root_dispatch(request):
    username = getattr(request, "subdomain", None)
    if username:
        return user_profile(request, username=username)
    return home(request)


def home(request):
    templates = Template.objects.filter(is_active=True)
    return render(request, "home-page.html", {'templates': templates})


def templates_page(request):
    templates = Template.objects.filter(is_active=True)
    return render(request, "templates-page.html", {'templates': templates})


def template_preview(request, template_name):
    try:
        template = Template.objects.get(template_file=template_name, is_active=True)
    except Template.DoesNotExist:
        messages.error(request, "Template not found.")
        return redirect("home")

    is_current = False
    if request.user.is_authenticated:
        is_current = UserTemplate.objects.filter(user=request.user, template=template).exists()

    return render(request, "template-preview-wrapper.html", {
        'template_name': template_name,
        'template': template,
        'is_current_template': is_current,
    })


@xframe_options_exempt
def template_preview_raw(request, template_name):
    try:
        template = Template.objects.get(template_file=template_name, is_active=True)
    except Template.DoesNotExist:
        messages.error(request, "Template not found.")
        return redirect("home")

    fullname = 'Your Name'
    initials = ''.join([part[0].upper() for part in fullname.split() if part])

    sample_data = {
        'user_fullname': fullname,
        'user_initials': initials,
        'profilephoto': None,
        'template_id': template.id,  
        'about': type('obj', (object,), {'about': 'Results-driven Senior Project Manager with 12+ years of experience leading cross-functional teams at top-tier technology companies. Skilled in Agile methodologies, stakeholder management, and delivering complex programmes on time and within budget. Passionate about fostering collaboration and driving innovation across global teams.'})(),
        'employment': [
            type('obj', (object,), {'employer_name': 'Apple', 'job_title': 'Senior Project Manager', 'description_of_duties': 'Managed end-to-end delivery of flagship product launches across hardware and software teams. Coordinated with 50+ stakeholders to align timelines, budgets, and quality standards.', 'start_date': '2021-04-01', 'end_date': None})(),
            type('obj', (object,), {'employer_name': 'Google', 'job_title': 'Technical Programme Manager', 'description_of_duties': 'Led cross-functional programmes for Google Cloud, overseeing roadmap planning, risk mitigation, and delivery of enterprise solutions to Fortune 500 clients.', 'start_date': '2017-09-15', 'end_date': '2021-03-31'})(),
            type('obj', (object,), {'employer_name': 'Microsoft', 'job_title': 'Project Coordinator', 'description_of_duties': 'Supported the Azure platform team with sprint planning, backlog grooming, and stakeholder reporting. Helped reduce delivery cycle times by 20%.', 'start_date': '2014-01-10', 'end_date': '2017-08-31'})(),
        ],
        'education': [
            type('obj', (object,), {'qualification': 'MBA Business Administration', 'institution_name': 'London Business School', 'start_date': '2012-09-01', 'end_date': '2014-06-30'})(),
            type('obj', (object,), {'qualification': 'BSc Business Management', 'institution_name': 'University of Manchester', 'start_date': '2008-09-01', 'end_date': '2012-06-30'})(),
        ],
        'certifications': [
            type('obj', (object,), {'name': 'PMP - Project Management Professional', 'issuer': 'Project Management Institute', 'date_issued': '2023-02-15'})(),
            type('obj', (object,), {'name': 'Certified ScrumMaster (CSM)', 'issuer': 'Scrum Alliance', 'date_issued': '2022-06-10'})(),
            type('obj', (object,), {'name': 'PRINCE2 Practitioner', 'issuer': 'Axelos', 'date_issued': '2020-11-20'})(),
        ],
        'portfolios': [
            type('obj', (object,), {'title': 'Global Product Launch', 'description': 'Led the coordinated launch of a new consumer device across 30 markets, managing timelines, vendor relationships, and cross-team dependencies to deliver on schedule.', 'link': '#', 'portfolio_photo': None})(),
            type('obj', (object,), {'title': 'Cloud Migration Programme', 'description': 'Directed a large-scale enterprise cloud migration programme for 15 clients, achieving 99.9% uptime during transition and reducing infrastructure costs by 35%.', 'link': '#', 'portfolio_photo': None})(),
            type('obj', (object,), {'title': 'Agile Transformation Initiative', 'description': 'Spearheaded the adoption of Agile practices across a 200-person engineering organisation, resulting in a 40% improvement in sprint velocity.', 'link': '#', 'portfolio_photo': None})(),
        ],
        'contact_methods': [
            type('obj', (object,), {
                'icon_class': 'fas fa-envelope',
                'get_contact_type_display': lambda: 'Email',
                'contact_type': 'email',
                'value': 'yourname@example.com',
                'label': '',
                'link_url': 'mailto:yourname@example.com',
            })(),
            type('obj', (object,), {
                'icon_class': 'fas fa-phone',
                'get_contact_type_display': lambda: 'Phone',
                'contact_type': 'phone',
                'value': '+1 234 567 8900',
                'label': '',
                'link_url': 'tel:+12345678900',
            })(),
            type('obj', (object,), {
                'icon_class': 'fab fa-linkedin-in',
                'get_contact_type_display': lambda: 'LinkedIn',
                'contact_type': 'linkedin',
                'value': 'yourname',
                'label': '',
                'link_url': 'https://www.linkedin.com/in/yourname',
            })(),
            type('obj', (object,), {
                'icon_class': 'fas fa-map-marker-alt',
                'get_contact_type_display': lambda: 'Address',
                'contact_type': 'address',
                'value': 'London, United Kingdom',
                'label': '',
                'link_url': '#',
            })(),
        ],
        'skill': type('obj', (object,), {'skills': ['Leadership', 'Stakeholder Management', 'Agile & Scrum', 'Strategic Planning', 'Risk Management', 'Team Building', 'Communication', 'Budgeting', 'Conflict Resolution', 'Problem Solving']})(),
    }

    return render(request, f"template-previews/{template_name}.html", sample_data)



@login_required
@csrf_exempt
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
        return redirect('template_preview', template_name=template.template_file)
    
    return redirect('home')


# render show portfolio page and handle contact form
# def user_profile(request, username):
#     target_user, data = get_user_data(username)

#     if not target_user:
#         messages.error(request, "The user you are looking for does not exist.")
#         return redirect("home")
def user_profile(request, username=None):
    # If someone reaches here via subdomain root
    if not username:
        username = getattr(request, "subdomain", None)

    if not username:
        return redirect("home")

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


@login_required
def share_subdomain(request, username):
    if request.user.username != username:
        messages.error(request, "You cannot access another user's share page.")
        return redirect("home")

    target_user, data = get_user_data(username)

    if not target_user:
        messages.error(request, "The user you are looking for does not exist.")
        return redirect("home")

    # Construct the subdomain URL
    if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host():
        # For local development, use localhost with subdomain
        subdomain_url = f"http://{username}.localhost:8000"
    else:
        # For production, use https and the configured base domain
        subdomain_url = f"https://{username}.{settings.BASE_DOMAIN}"

    context = {
        "target_user": target_user,
        "subdomain_url": subdomain_url,
        **data,  # Unpack the user-related data
    }
    return render(request, "share-subdomain.html", context)


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


# ── Contact CRUD ──────────────────────────────────────────────
@login_required
def add_contact_method(request):
    error_msg = "Error Adding Contact: "
    if request.method == "POST":
        form = ContactMethodForm(request.POST)
        if form.is_valid():
            cm = form.save(commit=False)
            cm.user = request.user
            cm.save()
            messages.success(request, "Contact added successfully.")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def edit_contact_method(request, id):
    error_msg = "Error Updating Contact: "
    cm = get_object_or_404(ContactMethod, id=id, user=request.user)
    if request.method == "POST":
        form = ContactMethodForm(request.POST, instance=cm)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully.")
        else:
            for field, errors in form.errors.items():
                label = form.fields[field].label or field
                for error in errors:
                    messages.error(request, f"{error_msg} '{label}': {error}")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_contact_method(request, id):
    cm = get_object_or_404(ContactMethod, id=id, user=request.user)
    if request.method == "POST":
        try:
            cm.delete()
            messages.success(request, "Contact deleted successfully.")
        except Exception as e:
            messages.error(
                request,
                f"An error occurred while deleting the Contact: {e}",
            )
    else:
        messages.error(request, "Invalid request method.")
    return redirect("edit_user_profile", username=request.user.username)


@login_required
def delete_all_contact_methods(request):
    if request.method == "POST":
        try:
            deleted_count, _ = ContactMethod.objects.filter(
                user=request.user
            ).delete()
            messages.success(
                request,
                f"All Contacts deleted successfully "
                f"({deleted_count} removed).",
            )
        except Exception as e:
            messages.error(
                request,
                f"An error occurred while deleting Contacts: {e}",
            )
    return redirect("edit_user_profile", username=request.user.username)


# ── CV content validation ────────────────────────────────────────────
import re as _re

# Keywords grouped by CV section — we require matches across
# at least 3 distinct groups to consider the document a CV.
_CV_KEYWORD_GROUPS = [
    # Contact / personal info
    [r'email', r'phone', r'linkedin', r'contact', r'address'],
    # Work experience
    [r'experience', r'employment', r'work\s+history', r'job\s+title',
     r'employer', r'responsibilities', r'duties'],
    # Education
    [r'education', r'university', r'college', r'degree', r'bachelor',
     r'master', r'diploma', r'qualification', r'school'],
    # Skills
    [r'skills?', r'proficien', r'competenc', r'technologies',
     r'tools', r'frameworks?', r'languages?'],
    # Certifications / achievements
    [r'certifi', r'accreditation', r'credential', r'license',
     r'award', r'achievement', r'accomplishment'],
    # Projects / portfolio
    [r'project', r'portfolio', r'publication', r'research'],
    # Generic CV / resume header markers
    [r'curriculum\s+vitae', r'\bresume\b', r'\bcv\b',
     r'professional\s+summary', r'objective', r'profile',
     r'career\s+summary', r'about\s+me', r'personal\s+statement'],
]


def _looks_like_cv(text: str, min_groups: int = 3) -> bool:
    """Return True if *text* matches keywords from at least *min_groups*
    distinct CV-related keyword groups."""
    text_lower = text.lower()
    matched = 0
    for group in _CV_KEYWORD_GROUPS:
        for kw in group:
            if _re.search(kw, text_lower):
                matched += 1
                break  # one match per group is enough
        if matched >= min_groups:
            return True
    return False


@login_required
def upload_cv(request):
    """Handle CV upload: extract text from PDF or Word (.docx), parse with
    Gemini, fall back to regex CVParser if Gemini fails, then save."""
    if request.method == "POST":
        form = CVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            cv_file = form.cleaned_data['cv_file']
            file_name = cv_file.name.lower()

            try:
                # --- 1. Extract raw text based on file type ---
                cv_text = ""

                if file_name.endswith('.docx'):
                    # Word document extraction
                    try:
                        import docx
                    except ImportError:
                        messages.error(
                            request,
                            "Word document processing library not installed. "
                            "Please contact administrator.",
                        )
                        return redirect(
                            "edit_user_profile",
                            username=request.user.username,
                        )

                    try:
                        document = docx.Document(cv_file)
                        cv_text = "\n".join(
                            para.text for para in document.paragraphs
                        )
                    except Exception as e:
                        logger.error("docx extraction failed: %s", e)
                        messages.error(
                            request,
                            "Could not read the Word document. Please ensure "
                            "it is a valid .docx file with readable text.",
                        )
                        return redirect(
                            "edit_user_profile",
                            username=request.user.username,
                        )

                else:
                    # PDF extraction
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
                        "The uploaded file appears to be empty or contains "
                        "no readable text.",
                    )
                    return redirect(
                        "edit_user_profile",
                        username=request.user.username,
                    )

                # --- 1b. Validate that the file looks like a CV ---
                if not _looks_like_cv(cv_text):
                    messages.error(
                        request,
                        "The uploaded file does not appear to be a CV "
                        "or resume. Please upload a valid CV.",
                    )
                    return redirect(
                        "edit_user_profile",
                        username=request.user.username,
                    )

                # --- 2. Parse with Vertex AI (primary) ---
                parsed_data = None
                try:
                    extractor = VertexAICVExtractor()
                    parsed_data = extractor.extract(cv_text)
                except (ValueError, ImportError) as exc:
                    # Vertex AI not configured or libraries not installed
                    logger.warning("Vertex AI unavailable: %s", exc)
                except Exception as exc:
                    logger.error("Vertex AI extraction error: %s", exc)

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
                        "Please ensure it's a valid file with "
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
    - ContactMethod & About → get_or_create then update.
    - Employment       → unique on (user, employer_name, job_title, start_date).
    - Education        → unique on (user, institution_name, qualification, start_date).
    - Certification    → unique on (user, name, issuer).
    - Portfolio        → unique on (user, title).
    """
    user = request.user

    # --- Contacts ---
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

    if email:
        ContactMethod.objects.get_or_create(
            user=user, contact_type='email', value=email,
            defaults={'label': ''},
        )
    if phone:
        ContactMethod.objects.get_or_create(
            user=user, contact_type='phone', value=phone,
            defaults={'label': ''},
        )
    if linkedin:
        ContactMethod.objects.get_or_create(
            user=user, contact_type='linkedin', value=linkedin,
            defaults={'label': ''},
        )

    # --- Country & Address ---
    country = parsed_data.get("country")
    address = parsed_data.get("address")
    if country or address:
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if country:
            profile.country = str(country).strip()[:100]
        if address:
            profile.address = str(address).strip()[:255]
        profile.save()

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


@login_required
def account_settings(request):
    """Account settings view for editing first name, last name, and username."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AccountSettingsForm(
            request.POST,
            instance=request.user,
            current_user=request.user,
        )
        if form.is_valid():
            form.save()
            profile.country = form.cleaned_data.get('country', '')
            profile.address = form.cleaned_data.get('address', '')
            profile.save()
            messages.success(request, "Account settings updated successfully.")
            return redirect('account_settings')
        else:
            # Username failed validation — save first/last name anyway
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name).strip()
            user.last_name = request.POST.get('last_name', user.last_name).strip()
            user.save(update_fields=['first_name', 'last_name'])
            # Still save profile fields
            profile.country = request.POST.get('country', profile.country).strip()
            profile.address = request.POST.get('address', profile.address).strip()
            profile.save()
            messages.success(request, "Name updated successfully.")
            for field, errors in form.errors.items():
                label = form.fields[field].label or field.capitalize()
                for error in errors:
                    messages.error(request, f"{label}: {error}")
    else:
        form = AccountSettingsForm(
            instance=request.user,
            current_user=request.user,
            initial={
                'country': profile.country,
                'address': profile.address,
            },
        )
    return render(request, 'account-settings.html', {'form': form})


def custom_404(request, exception):
    """Custom 404 error handler."""
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 error handler."""
    return render(request, '500.html', status=500)
