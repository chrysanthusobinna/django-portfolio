from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from unittest.mock import patch
from portfolio_app.models import Portfolio
from portfolio_app.forms import PortfolioForm


class AddPortfolioViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.url = reverse('add_portfolio')

    @patch('portfolio_app.views.validate_image_file')  # Mock the validate_image_file function
    @patch('portfolio_app.views.PortfolioForm')  # Mock the PortfolioForm
    def test_add_portfolio_valid(self, mock_portfolio_form, mock_validate_image_file):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Mock the validate_image_file function to return valid response
        mock_validate_image_file.return_value = (True, None)

        # Mock the form to simulate successful form submission
        mock_form_instance = mock_portfolio_form.return_value
        mock_form_instance.is_valid.return_value = True
        mock_form_instance.save.return_value = Portfolio(user=self.user)

        response = self.client.post(self.url, data={
            'title': 'Portfolio Title',
            'description': 'Portfolio Description',
            'portfolio_photo': 'fakephoto.jpg'
        })

        # Check that the portfolio was saved and success message was shown
        self.assertEqual(Portfolio.objects.count(), 1)
        self.assertRedirects(response, reverse('edit_user_profile', args=[self.user.username]))

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Portfolio added successfully.' for msg in messages))

    @patch('portfolio_app.views.validate_image_file')  # Mock the validate_image_file function
    @patch('portfolio_app.views.PortfolioForm')  # Mock the PortfolioForm
    def test_add_portfolio_invalid_form(self, mock_portfolio_form, mock_validate_image_file):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Mock the validate_image_file function to return valid response
        mock_validate_image_file.return_value = (True, None)

        # Mock the form to simulate invalid form submission
        mock_form_instance = mock_portfolio_form.return_value
        mock_form_instance.is_valid.return_value = False
        mock_form_instance.errors = {'title': ['This field is required.']}

        response = self.client.post(self.url, data={
            'title': '',
            'description': 'Portfolio Description',
            'portfolio_photo': 'fakephoto.jpg'
        })

        # Check that no portfolio was saved
        self.assertEqual(Portfolio.objects.count(), 0)

        # Check that the form errors were shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Error Adding Portfolio:' in msg.message for msg in messages))

    @patch('portfolio_app.views.validate_image_file')  # Mock the validate_image_file function
    def test_add_portfolio_invalid_image(self, mock_validate_image_file):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Mock the validate_image_file function to return an error
        mock_validate_image_file.return_value = (False, 'Invalid image file.')

        response = self.client.post(self.url, data={
            'title': 'Portfolio Title',
            'description': 'Portfolio Description',
            'portfolio_photo': 'fakephoto.jpg'
        })

        # Check that no portfolio was saved
        self.assertEqual(Portfolio.objects.count(), 0)

        # Check that the error message was shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Invalid image file.' for msg in messages))

    def test_add_portfolio_unauthenticated(self):
        response = self.client.post(self.url, data={
            'title': 'Portfolio Title',
            'description': 'Portfolio Description',
            'portfolio_photo': 'fakephoto.jpg'
        })

        # Check that the user is redirected to the login page
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
