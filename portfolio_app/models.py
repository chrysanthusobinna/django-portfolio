from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return f"{self.job_title} at {self.employer_name}"

# Education Section Model
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    qualification = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.qualification} from {self.institution_name}"

# Certification Section Model
class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_issued = models.DateField()

    def __str__(self):
        return f"{self.name} by {self.issuer}"

# Portfolio Section Model
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

# Contact Section Model
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    linkedin = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Contact Info for {self.user.username}"
