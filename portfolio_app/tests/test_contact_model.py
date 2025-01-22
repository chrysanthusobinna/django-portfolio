from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import Contact

class ContactModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_contact_creation(self):
        # Create a Contact instance
        contact = Contact.objects.create(
            user=self.user,
            phone_number='123-456-7890',
            email_address='test@example.com',
            linkedin='https://www.linkedin.com/in/testuser'
        )
        self.assertEqual(contact.user, self.user)
        self.assertEqual(contact.phone_number, '123-456-7890')
        self.assertEqual(contact.email_address, 'test@example.com')
        self.assertEqual(contact.linkedin, 'https://www.linkedin.com/in/testuser')
        self.assertEqual(str(contact), f"Contact Info for {self.user.username}")

    def test_contact_update(self):
        # Create and update a Contact instance
        contact = Contact.objects.create(
            user=self.user,
            phone_number='123-456-7890',
            email_address='test@example.com',
            linkedin='https://www.linkedin.com/in/testuser'
        )
        contact.phone_number = '098-765-4321'
        contact.save()

        # Retrieve and check updated value
        updated_contact = Contact.objects.get(id=contact.id)
        self.assertEqual(updated_contact.phone_number, '098-765-4321')

    def test_contact_delete(self):
        # Create and delete a Contact instance
        contact = Contact.objects.create(
            user=self.user,
            phone_number='123-456-7890',
            email_address='test@example.com',
            linkedin='https://www.linkedin.com/in/testuser'
        )
        contact_id = contact.id
        contact.delete()

        # Ensure the instance is deleted
        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(id=contact_id)
