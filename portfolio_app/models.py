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


# Contact Section Model
class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contacts')
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    linkedin = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Contact Info for {self.user.username}"
