from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User

from .models import (
    ContactMethod,
    Portfolio,
    Certification,
    Education,
    Employment,
    About,
    Profilephoto
)


class AccountSettingsForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
        })
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'id': 'id_username',
        })
    )
    COUNTRY_LIST = [
        'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
        'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia',
        'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
        'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan',
        'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
        'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde',
        'Cambodia', 'Cameroon', 'Canada', 'Central African Republic',
        'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo',
        'Congo (DRC)', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba',
        'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica',
        'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
        'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia',
        'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia',
        'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea',
        'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary',
        'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland',
        'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
        'Kenya', 'Kiribati', 'North Korea', 'South Korea', 'Kuwait',
        'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia',
        'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar',
        'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
        'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
        'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro',
        'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal',
        'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria',
        'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau',
        'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru',
        'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
        'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia',
        'Saint Vincent and the Grenadines', 'Samoa', 'San Marino',
        'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
        'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
        'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan',
        'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden',
        'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
        'Thailand', 'Timor-Leste', 'Togo', 'Tonga',
        'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
        'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
        'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
        'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen',
        'Zambia', 'Zimbabwe',
    ]

    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'list': 'country-list',
            'placeholder': 'Type to search country...',
            'autocomplete': 'off',
        })
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your address',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if country and country not in self.COUNTRY_LIST:
            raise forms.ValidationError(
                'Please select a valid country from the list.'
            )
        return country

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.current_user and username != self.current_user.username:
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError(
                    'This username is already taken. Please choose another.'
                )
        return username


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
