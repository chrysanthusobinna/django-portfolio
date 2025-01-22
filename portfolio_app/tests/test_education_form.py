from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.forms import EducationForm
from portfolio_app.models import Education
import datetime

class EducationFormTests(TestCase):
    def setUp(self):
        # Create a test user to associate with the education
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_education_form_valid(self):
        # Valid form data
        form_data = {
            'qualification': 'Bachelor of Science',
            'institution_name': 'Example University',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01'
        }
        form = EducationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_education_form_invalid_missing_qualification(self):
        # Invalid form data (missing qualification)
        form_data = {
            'institution_name': 'Example University',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01'
        }
        form = EducationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('qualification', form.errors)

    def test_education_form_invalid_missing_institution_name(self):
        # Invalid form data (missing institution_name)
        form_data = {
            'qualification': 'Bachelor of Science',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01'
        }
        form = EducationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('institution_name', form.errors)

    def test_education_form_invalid_missing_start_date(self):
        # Invalid form data (missing start_date)
        form_data = {
            'qualification': 'Bachelor of Science',
            'institution_name': 'Example University',
            'end_date': '2023-01-01'
        }
        form = EducationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)

    def test_education_form_valid_missing_end_date(self):
        # Valid form data (end_date is optional)
        form_data = {
            'qualification': 'Bachelor of Science',
            'institution_name': 'Example University',
            'start_date': '2020-01-01'
        }
        form = EducationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_education_form_save(self):
        # Test saving valid form data to the database
        form_data = {
            'qualification': 'Bachelor of Science',
            'institution_name': 'Example University',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01'
        }
        form = EducationForm(data=form_data)
        self.assertTrue(form.is_valid())
        education = form.save(commit=False)
        education.user = self.user  # Associate the education with the test user
        education.save()

        # Verify the data is saved correctly
        saved_education = Education.objects.get(id=education.id)
        self.assertEqual(saved_education.qualification, form_data['qualification'])
        self.assertEqual(saved_education.institution_name, form_data['institution_name'])
        self.assertEqual(saved_education.start_date, datetime.date.fromisoformat(form_data['start_date']))
        self.assertEqual(saved_education.end_date, datetime.date.fromisoformat(form_data['end_date']))
