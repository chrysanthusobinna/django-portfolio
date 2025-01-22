from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Profilephoto
from cloudinary import CloudinaryResource


class DeleteProfilePhotoViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # URL for deleting the profile photo
        self.delete_profile_photo_url = reverse('delete_profile_photo')
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

        # Create a Profilephoto entry with a CloudinaryField for the test user
        self.profile_photo = Profilephoto.objects.create(
            user=self.user,
            profile_photo=CloudinaryResource('sample-image-id')  # Mock Cloudinary resource
        )

    def test_delete_profile_photo_success(self):
        # Test successfully deleting the profile photo
        response = self.client.post(self.delete_profile_photo_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify the profile photo is deleted from the database
        self.assertFalse(Profilephoto.objects.filter(user=self.user).exists())

        # Check for success messages
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Profile photo deleted successfully.' in str(message) for message in messages))

    def test_delete_profile_photo_no_entry(self):
        # Delete the profile photo before testing
        self.profile_photo.delete()

        # Test trying to delete a non-existent profile photo
        response = self.client.post(self.delete_profile_photo_url)
        self.assertEqual(response.status_code, 404)

    def test_delete_profile_photo_invalid_method(self):
        # Test using a GET request instead of POST
        response = self.client.get(self.delete_profile_photo_url)
        self.assertRedirects(response, self.redirect_url)

        # Verify the profile photo still exists in the database
        self.assertTrue(Profilephoto.objects.filter(user=self.user).exists())

        # redirect 
        self.assertRedirects(response, self.redirect_url)

    def test_delete_profile_photo_no_login(self):
        # Log out the user
        self.client.logout()

        # Test trying to access the delete_profile_photo view without logging in
        response = self.client.post(self.delete_profile_photo_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.delete_profile_photo_url}")

        # Verify the profile photo is not deleted
        self.assertTrue(Profilephoto.objects.filter(user=self.user).exists())
