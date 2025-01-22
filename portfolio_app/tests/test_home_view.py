from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from unittest.mock import patch
from django.conf import settings


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.valid_post_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }

    @patch('portfolio_app.views.send_contact_email')  # Mock the send_contact_email function
    def test_home_view_post_valid(self, mock_send_contact_email):
        # Mock the send_contact_email function to return success
        mock_send_contact_email.return_value = (True, None)

        response = self.client.post(self.url, data=self.valid_post_data)

        # Check that the user is redirected to 'home'
        self.assertRedirects(response, self.url)

        # Check that the success message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Your message has been sent successfully!' for msg in messages))

        # Check that send_contact_email was called with correct arguments
        full_message = f"Name: John Doe\nEmail: john.doe@example.com\n\nThis is a test message."
        mock_send_contact_email.assert_called_once_with(
            'Test Subject', full_message, [settings.SITE_CONTACT_EMAIL_ADDRESS]
        )

    @patch('portfolio_app.views.send_contact_email')  # Mock the send_contact_email function
    def test_home_view_post_invalid(self, mock_send_contact_email):
        # Mock the send_contact_email function to return failure
        mock_send_contact_email.return_value = (False, 'Error sending email.')

        response = self.client.post(self.url, data=self.valid_post_data)

        # Check that the user is redirected to 'home'
        self.assertRedirects(response, self.url)

        # Check that the error message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Error sending email.' for msg in messages))

    def test_home_view_get(self):
        response = self.client.get(self.url)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'home-page.html')
