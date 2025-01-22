from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Contact

class ContactDeleteViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # URL for deleting contact information
        self.contact_delete_url = reverse('contact_delete')
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_contact_delete_success(self):
        # Create a contact entry for the user
        Contact.objects.create(
            user=self.user,
            phone_number='9876543210',
            email_address='oldemail@example.com',
            linkedin='https://www.linkedin.com/in/olduser',
        )

        # Perform the delete action
        response = self.client.post(self.contact_delete_url)

        # Check redirection after successful deletion
        self.assertRedirects(response, self.redirect_url)

        # Verify the contact information is deleted from the database
        self.assertFalse(Contact.objects.filter(user=self.user).exists())

        # Check for success message
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Contact deleted successfully.' in str(message) for message in messages))

    def test_contact_delete_no_contact(self):
        # Attempt to delete when no contact exists for the user
        response = self.client.post(self.contact_delete_url)

        # Check redirection after attempting to delete non-existent contact
        self.assertRedirects(response, self.redirect_url)

        # Verify no contact information is deleted (since none exists)
        self.assertFalse(Contact.objects.filter(user=self.user).exists())

        # Check for error message indicating contact was not found
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Contact not found.' in str(message) for message in messages))

    def test_contact_delete_no_login(self):
        # Log out the user
        self.client.logout()

        # Attempt to access the contact_delete view without logging in
        response = self.client.post(self.contact_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.contact_delete_url}")

        # Verify no contact information is deleted
        self.assertFalse(Contact.objects.filter(user=self.user).exists())
