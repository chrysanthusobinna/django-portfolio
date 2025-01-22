from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import About

class SaveAboutViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # URL for saving the about section
        self.save_about_url = reverse('save_about')
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_save_about_create(self):
        # Test creating a new About entry
        response = self.client.post(self.save_about_url, {'about': 'This is my about section.'})
        self.assertRedirects(response, self.redirect_url)

        # Verify the About entry is created in the database
        about = About.objects.get(user=self.user)
        self.assertEqual(about.about, 'This is my about section.')

    def test_save_about_update(self):
        # Create an initial About entry
        About.objects.create(user=self.user, about='Old about section.')

        # Test updating the About entry
        response = self.client.post(self.save_about_url, {'about': 'Updated about section.'})
        self.assertRedirects(response, self.redirect_url)

        # Verify the About entry is updated in the database
        about = About.objects.get(user=self.user)
        self.assertEqual(about.about, 'Updated about section.')

    def test_save_about_invalid_form(self):
        # Test with invalid form data (e.g., empty 'about' field)
        response = self.client.post(self.save_about_url, {'about': ''})
        self.assertRedirects(response, self.redirect_url)

        # Verify the About entry is not created in the database
        about = About.objects.get(user=self.user)
        self.assertEqual(about.about, '')


        # Check for error messages
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Error Saving About' in str(message) for message in messages))

    def test_save_about_no_login(self):
        # Log out the user
        self.client.logout()

        # Test accessing the save_about view without logging in
        response = self.client.post(self.save_about_url, {'about': 'This is my about section.'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.save_about_url}")

        # Verify the About entry is not created in the database
        self.assertFalse(About.objects.filter(user=self.user).exists())
