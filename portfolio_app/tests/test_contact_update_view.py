from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Contact

class ContactUpdateViewTests(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # URL for updating contact information
        self.contact_update_url = reverse('contact_update')
        self.redirect_url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_contact_update_create_success(self):
        # Data for creating a new contact
        data = {
            'phone_number': '1234567890',
            'email_address': 'testuser@example.com',
            'linkedin': 'https://www.linkedin.com/in/testuser',
        }

        response = self.client.post(self.contact_update_url, data)

        # Check redirection after successful creation
        self.assertRedirects(response, self.redirect_url)

        # Verify the contact information is saved in the database
        contact = Contact.objects.get(user=self.user)
        self.assertEqual(contact.phone_number, data['phone_number'])
        self.assertEqual(contact.email_address, data['email_address'])
        self.assertEqual(contact.linkedin, data['linkedin'])

        # Check for success messages
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Contact updated successfully.' in str(message) for message in messages))

    def test_contact_update_edit_success(self):
        # Create a contact entry for the user
        Contact.objects.create(
            user=self.user,
            phone_number='9876543210',
            email_address='oldemail@example.com',
            linkedin='https://www.linkedin.com/in/olduser',
        )

        # Data for updating the contact
        updated_data = {
            'phone_number': '1112223333',
            'email_address': 'newemail@example.com',
            'linkedin': 'https://www.linkedin.com/in/newuser',
        }

        response = self.client.post(self.contact_update_url, updated_data)

        # Check redirection after successful update
        self.assertRedirects(response, self.redirect_url)

        # Verify the contact information is updated in the database
        contact = Contact.objects.get(user=self.user)
        self.assertEqual(contact.phone_number, updated_data['phone_number'])
        self.assertEqual(contact.email_address, updated_data['email_address'])
        self.assertEqual(contact.linkedin, updated_data['linkedin'])

        # Check for success messages
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Contact updated successfully.' in str(message) for message in messages))

    def test_contact_update_form_errors(self):
        # Submit invalid data to trigger form errors
        invalid_data = {
            'phone_number': '',  # Empty phone number
            'email_address': 'invalid-email',  # Invalid email format
        }

        response = self.client.post(self.contact_update_url, invalid_data)

        # Check redirection after form errors
        self.assertRedirects(response, self.redirect_url)

        # Verify no contact information is saved in the database
        self.assertFalse(Contact.objects.filter(user=self.user).exists())

        # Check for specific error messages for missing phone number and invalid email
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Error Saving Contact:' in str(message) for message in messages))
        self.assertTrue(any('Error Saving Contact:' in str(message) for message in messages))

    def test_contact_update_no_login(self):
        # Log out the user
        self.client.logout()

        # Attempt to access the contact_update view without logging in
        response = self.client.post(self.contact_update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.contact_update_url}")

        # Verify no contact information is saved in the database
        self.assertFalse(Contact.objects.filter(user=self.user).exists())
