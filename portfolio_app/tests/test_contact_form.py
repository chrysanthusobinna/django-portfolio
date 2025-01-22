from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.forms import ContactForm
from portfolio_app.models import Contact

class ContactFormTests(TestCase):
    def setUp(self):
        # Create a test user to associate with the contact
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_contact_form_valid(self):
        # Valid data for the contact form
        data = {
            'phone_number': '1234567890',
            'email_address': 'test@example.com',
            'linkedin': 'https://www.linkedin.com/in/testuser',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_phone_number(self):
        # Invalid phone number (empty)
        data = {
            'phone_number': '',
            'email_address': 'test@example.com',
            'linkedin': 'https://www.linkedin.com/in/testuser',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['phone_number'])

    def test_contact_form_invalid_email(self):
        # Invalid email address (incorrect format)
        data = {
            'phone_number': '1234567890',
            'email_address': 'invalid-email',
            'linkedin': 'https://www.linkedin.com/in/testuser',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email_address'])

    def test_contact_form_invalid_linkedin(self):
        # Invalid LinkedIn URL (incorrect format)
        data = {
            'phone_number': '1234567890',
            'email_address': 'test@example.com',
            'linkedin': 'invalid-linkedin-url',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid URL.', form.errors['linkedin'])

    def test_contact_form_save(self):
        # Test saving valid form data to the database
        data = {
            'phone_number': '1234567890',
            'email_address': 'test@example.com',
            'linkedin': 'https://www.linkedin.com/in/testuser',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
        contact = form.save(commit=False)
        contact.user = self.user  # Associate the test user with the contact
        contact.save()

        # Verify the data is saved correctly
        saved_contact = Contact.objects.get(user=self.user)
        self.assertEqual(saved_contact.phone_number, data['phone_number'])
        self.assertEqual(saved_contact.email_address, data['email_address'])
        self.assertEqual(saved_contact.linkedin, data['linkedin'])
