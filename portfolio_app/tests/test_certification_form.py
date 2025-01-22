from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.forms import CertificationForm
from portfolio_app.models import Certification
import datetime

class CertificationFormTests(TestCase):
    def setUp(self):
        # Create a test user to associate with the certification
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_certification_form_valid(self):
        # Valid form data
        form_data = {
            'name': 'Certified Python Developer',
            'issuer': 'Python Institute',
            'date_issued': '2023-10-10'
        }
        form = CertificationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_certification_form_invalid_missing_name(self):
        # Invalid form data (missing name)
        form_data = {
            'issuer': 'Python Institute',
            'date_issued': '2023-10-10'
        }
        form = CertificationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_certification_form_invalid_missing_issuer(self):
        # Invalid form data (missing issuer)
        form_data = {
            'name': 'Certified Python Developer',
            'date_issued': '2023-10-10'
        }
        form = CertificationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('issuer', form.errors)

    def test_certification_form_invalid_missing_date_issued(self):
        # Invalid form data (missing date_issued)
        form_data = {
            'name': 'Certified Python Developer',
            'issuer': 'Python Institute'
        }
        form = CertificationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_issued', form.errors)

    def test_certification_form_save(self):
        # Test saving valid form data to the database
        form_data = {
            'name': 'Certified Python Developer',
            'issuer': 'Python Institute',
            'date_issued': '2023-10-10'
        }
        form = CertificationForm(data=form_data)
        self.assertTrue(form.is_valid())
        certification = form.save(commit=False)
        certification.user = self.user  # Associate the certification with the test user
        certification.save()

        # Verify the data is saved correctly
        saved_certification = Certification.objects.get(id=certification.id)
        self.assertEqual(saved_certification.name, form_data['name'])
        self.assertEqual(saved_certification.issuer, form_data['issuer'])
        self.assertEqual(saved_certification.date_issued, datetime.date.fromisoformat(form_data['date_issued']))
