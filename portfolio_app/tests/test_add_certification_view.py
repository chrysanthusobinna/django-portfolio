from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from portfolio_app.models import Certification
from django.contrib.messages import get_messages
from portfolio_app.forms import CertificationForm

class AddCertificationViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.client = self.client_class()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.url = reverse('add_certification')  # URL for the 'add_certification' view

    def test_add_certification_valid(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Prepare valid form data
        form_data = {
            'name': 'Certified Python Developer',
            'issuer': 'Python Institute',
            'date_issued': '2023-01-01'
        }

        # Post the form data
        response = self.client.post(self.url, data=form_data)

        # Check that the certification was added to the database
        self.assertEqual(Certification.objects.count(), 1)
        certification = Certification.objects.first()
        self.assertEqual(certification.name, 'Certified Python Developer')
        self.assertEqual(certification.issuer, 'Python Institute')
        self.assertEqual(str(certification.date_issued), '2023-01-01')

        # Check that the success message was shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Certification added successfully.' for msg in messages))

        # Check that the user was redirected back to their profile page
        self.assertRedirects(response, reverse('edit_user_profile', args=[self.user.username]))

    def test_add_certification_invalid(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Prepare invalid form data (missing date_issued)
        form_data = {
            'name': 'Certified Python Developer',
            'issuer': 'Python Institute',
            'date_issued': ''
        }

        # Post the invalid form data
        response = self.client.post(self.url, data=form_data)

        # Check that no certification was added to the database
        self.assertEqual(Certification.objects.count(), 0)

        # Check that the error message was shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message.startswith('Error Adding Certification:') for msg in messages))

        # Check that the user was redirected back to their profile page
        self.assertRedirects(response, reverse('edit_user_profile', args=[self.user.username]))
