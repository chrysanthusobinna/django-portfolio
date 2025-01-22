from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from portfolio_app.models import Certification
from django.contrib.messages import get_messages

class DeleteCertificationViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.client = self.client_class()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.certification = Certification.objects.create(
            user=self.user,
            name="Certified Python Developer",
            issuer="Python Institute",
            date_issued="2023-01-01"
        )
        self.url = reverse('delete_certification', args=[self.certification.id])  # URL for the 'delete_certification' view

    def test_delete_certification_valid(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Post the delete request
        response = self.client.post(self.url)

        # Check that the certification was deleted
        with self.assertRaises(Certification.DoesNotExist):
            Certification.objects.get(id=self.certification.id)

        # Check that the success message was shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Certification deleted successfully.' for msg in messages))

        # Check that the user was redirected back to their profile page
        self.assertRedirects(response, reverse('edit_user_profile', args=[self.user.username]))

    def test_delete_certification_invalid_method(self):
        # Log in as the test user
        self.client.login(username='testuser', password='password123')

        # Get request instead of post
        response = self.client.get(self.url)

        # Check that the certification is still in the database
        Certification.objects.get(id=self.certification.id)

        # Check that the error message was shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == 'Invalid request method.' for msg in messages))

        # Check that the user was redirected back to their profile page
        self.assertRedirects(response, reverse('edit_user_profile', args=[self.user.username]))

    def test_delete_certification_not_owner(self):
        # Create another user and log in as them
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='password123'
        )
        self.client.login(username='otheruser', password='password123')

        # Try to delete the certification of the first user
        response = self.client.post(self.url)

        # Check that the certification was not deleted
        self.assertTrue(Certification.objects.filter(id=self.certification.id).exists())

        # Check that the error message was shown
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 404)