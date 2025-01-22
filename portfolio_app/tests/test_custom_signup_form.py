from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from portfolio_app.forms import CustomSignupForm

class CustomSignupFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_custom_signup_form_valid(self):
        # Valid form data
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser'
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_signup_form_invalid_missing_first_name(self):
        # Invalid form data (missing first_name)
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'last_name': 'User',
            'username': 'testuser'
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_custom_signup_form_invalid_missing_last_name(self):
        # Invalid form data (missing last_name)
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'username': 'testuser'
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_custom_signup_form_invalid_missing_username(self):
        # Invalid form data (missing username)
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_custom_signup_form_save(self):
        # Test saving valid form data to the database
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser'
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Create a mock request with a session
        request = self.factory.post('/accounts/signup/', form_data)
        request.session = self.client.session

        user = form.save(request)

        # Verify the data is saved correctly
        saved_user = User.objects.get(id=user.id)
        self.assertEqual(saved_user.email, form_data['email'])
        self.assertEqual(saved_user.first_name, form_data['first_name'])
        self.assertEqual(saved_user.last_name, form_data['last_name'])
        self.assertEqual(saved_user.username, form_data['username'])
