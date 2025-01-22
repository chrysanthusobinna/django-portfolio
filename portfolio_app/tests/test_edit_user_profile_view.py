from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from unittest.mock import patch


class EditUserProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.target_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.url = reverse('edit_user_profile', args=[self.target_user.username])

    @patch('portfolio_app.views.get_user_data')  # Mock the get_user_data function
    def test_edit_user_profile_authenticated_valid_user(self, mock_get_user_data):
        # Log in as the target user
        self.client.login(username='testuser', password='password123')

        # Mock the get_user_data function to return the user and additional data
        mock_get_user_data.return_value = (self.target_user, {'key': 'value'})

        response = self.client.get(self.url)

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'edit-user-portfolio.html')

        # Check that the context contains the expected data
        self.assertEqual(response.context['target_user'], self.target_user)
        self.assertIn('key', response.context)

    @patch('portfolio_app.views.get_user_data')  # Mock the get_user_data function
    def test_edit_user_profile_authenticated_invalid_user(self, mock_get_user_data):
        # Log in as the target user
        self.client.login(username='testuser', password='password123')

        # Mock the get_user_data function to return None for the user
        mock_get_user_data.return_value = (None, {})

        response = self.client.get(self.url)

        # Check that the user is redirected to 'home'
        self.assertRedirects(response, reverse('home'))

        # Check that the error message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'The user you are looking for does not exist.' for msg in messages))

    def test_edit_user_profile_unauthenticated(self):
        response = self.client.get(self.url)

        # Check that the user is redirected to the login page
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
