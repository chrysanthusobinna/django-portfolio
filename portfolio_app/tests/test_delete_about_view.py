from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import About

class DeleteAboutViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # URL for deleting the about section
        self.delete_about_url = reverse('delete_about')
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

        # Create an About entry for the test user
        self.about = About.objects.create(user=self.user, about='This is my about section.')

    def test_delete_about_success(self):
        # Test successfully deleting the About entry
        response = self.client.post(self.delete_about_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify the About entry is deleted from the database
        self.assertFalse(About.objects.filter(user=self.user).exists())

        # Check for success messages
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('About section deleted successfully.' in str(message) for message in messages))

    def test_delete_about_no_entry(self):
        # Delete the About entry before testing
        self.about.delete()

        # Test trying to delete a non-existent About entry
        response = self.client.post(self.delete_about_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_about_invalid_method(self):
        # Test using a GET request instead of POST
        response = self.client.get(self.delete_about_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify the About entry still exists in the database
        self.assertTrue(About.objects.filter(user=self.user).exists())

        # should redirect back
        self.assertRedirects(response, self.redirect_url)

    def test_delete_about_no_login(self):
        # Log out the user
        self.client.logout()

        # Test trying to access the delete_about view without logging in
        response = self.client.post(self.delete_about_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.delete_about_url}")

        # Verify the About entry is not deleted
        self.assertTrue(About.objects.filter(user=self.user).exists())
