from allauth.account.forms import SignupForm
from django import forms

from .models import (
    ContactMethod,
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


class ContactMethodForm(forms.ModelForm):
    class Meta:
        model = ContactMethod
        fields = ['contact_type', 'value', 'label']
        widgets = {
            'contact_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number, email, URL, or username',
            }),
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Work, Personal (optional)',
            }),
        }
        labels = {
            'contact_type': 'Contact Type',
            'value': 'Value',
            'label': 'Label (optional)',
        }


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


class CVUploadForm(forms.Form):
    cv_file = forms.FileField(
        label='Upload CV (PDF format)',
        required=True,
        widget=forms.FileInput(attrs={
            'accept': '.pdf',
            'class': 'form-control'
        })
    )
    
    def clean_cv_file(self):
        cv_file = self.cleaned_data.get('cv_file')
        
        if cv_file:
            # Check file extension
            if not cv_file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            
            # Check file size (max 10MB)
            if cv_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10MB.')
        
        return cv_file
