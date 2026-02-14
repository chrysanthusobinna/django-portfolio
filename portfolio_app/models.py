import json

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Template model
class Template(models.Model):
    name = models.CharField(max_length=255)
    template_file = models.CharField(max_length=255)  # maps to template file name
    description = models.TextField()
    image_path = models.CharField(max_length=255)  # path to template preview image
    tag = models.CharField(max_length=50, default='Classic')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# UserTemplate model to store user's selected template
class UserTemplate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    selected_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.template.name if self.template else 'No template'}"


# Profile photo model
class Profilephoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return f"Profile photo for {self.user.username}"


# About model
class About(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()

    def __str__(self):
        return f"About {self.user.username}"


# Employment model
class Employment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description_of_duties = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.employer_name}"


# Education Section Model
class Education(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='educations')
    qualification = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.qualification} from {self.institution_name}"


# Certification Section Model
class Certification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_issued = models.DateField()

    def __str__(self):
        return f"{self.name} by {self.issuer}"


# Portfolio Section Model
class Portfolio(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(null=True, blank=True)
    portfolio_photo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.title


# Flexible Contact Method model
class ContactMethod(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]

    # Maps each type to (Font Awesome icon class, URL prefix)
    CONTACT_TYPE_META = {
        'phone':     ('fas fa-phone',          'tel:'),
        'email':     ('fas fa-envelope',       'mailto:'),
        'whatsapp':  ('fab fa-whatsapp',       'https://wa.me/'),
        'instagram': ('fab fa-instagram',      'https://instagram.com/'),
        'facebook':  ('fab fa-facebook',       'https://facebook.com/'),
        'linkedin':  ('fab fa-linkedin-in',    'https://linkedin.com/in/'),
        'twitter':   ('fab fa-x-twitter',      'https://x.com/'),
        'website':   ('fas fa-globe',          ''),
        'other':     ('fas fa-address-card',   ''),
    }

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contact_methods')
    contact_type = models.CharField(
        max_length=20, choices=CONTACT_TYPE_CHOICES, default='phone')
    value = models.CharField(max_length=255)
    label = models.CharField(
        max_length=50, blank=True, default='',
        help_text='Optional label, e.g. "Work", "Personal"')

    class Meta:
        ordering = ['contact_type', 'id']

    def __str__(self):
        display = f"{self.get_contact_type_display()}: {self.value}"
        if self.label:
            display += f" ({self.label})"
        return display

    @property
    def icon_class(self):
        """Return the Font Awesome CSS class for this contact type."""
        return self.CONTACT_TYPE_META.get(
            self.contact_type, ('fas fa-address-card', ''))[0]

    @property
    def link_url(self):
        """Return a clickable URL for this contact method."""
        prefix = self.CONTACT_TYPE_META.get(
            self.contact_type, ('', ''))[1]

        # If value already looks like a full URL, use it as-is
        if self.value.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return self.value

        if prefix:
            return f"{prefix}{self.value}"
        return self.value


# Skill model – stores skills as a JSON array (e.g. ["Leadership", "Excel"])
class Skill(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Skills for {self.user.username}"

    def get_skills_list(self):
        """Return skills as a Python list, handling edge cases safely."""
        if isinstance(self.skills, list):
            return self.skills
        if isinstance(self.skills, str):
            try:
                parsed = json.loads(self.skills)
                return parsed if isinstance(parsed, list) else []
            except (json.JSONDecodeError, TypeError):
                # Treat as comma-separated string
                return [s.strip() for s in self.skills.split(",") if s.strip()]
        return []

    def get_skills_json(self):
        """Return skills as a JSON string for the hidden input."""
        return json.dumps(self.get_skills_list())
