from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio_app.models import Education

class AddEducationViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.url = reverse('edit_user_profile', kwargs={'username': self.user.username})

    def test_add_education_valid(self):
        # Test adding a valid education entry
        form_data = {
            'qualification': 'BSc Computer Science',
            'institution_name': 'University of Test',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(reverse('add_education'), data=form_data)
        self.assertRedirects(response, self.url)
        self.assertEqual(Education.objects.count(), 1)
        education = Education.objects.first()
        self.assertEqual(education.qualification, 'BSc Computer Science')
        self.assertEqual(education.institution_name, 'University of Test')
        self.assertEqual(str(education.start_date), '2020-01-01')
        self.assertEqual(str(education.end_date), '2023-01-01')
        self.assertEqual(education.user, self.user)

    def test_add_education_invalid(self):
        # Test adding an invalid education entry
        form_data = {
            'qualification': '',  # Missing required field
            'institution_name': 'University of Test',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
        }
        response = self.client.post(reverse('add_education'), data=form_data)
        self.assertRedirects(response, self.url)
        self.assertEqual(Education.objects.count(), 0)
