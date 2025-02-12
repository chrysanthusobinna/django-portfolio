from allauth.account.forms import SignupForm
from django import forms

from .models import (
    Contact,
    Portfolio,
    Certification,
    Education,
    Employment,
    About,
    Profilephoto
)


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30, label="First Name", required=True)

    last_name = forms.CharField(
        max_length=30, label="Last Name", required=True)

    username = forms.CharField(
        max_length=30, label="Username", required=True)

    def save(self, request):
        user = super(
            CustomSignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.save()
        return user


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'phone_number', 'email_address', 'linkedin'
            ]


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'link', 'portfolio_photo']


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = [
            'name', 'issuer', 'date_issued'
            ]


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'qualification', 'institution_name', 'start_date', 'end_date'
            ]


class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = ['employer_name', 'job_title', 'description_of_duties', 'start_date', 'end_date']  # noqa


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['about']


class ProfilephotoForm(forms.ModelForm):
    class Meta:
        model = Profilephoto
        fields = ['profile_photo']
