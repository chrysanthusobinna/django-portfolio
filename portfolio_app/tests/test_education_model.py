from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import Education
import datetime

class EducationModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_education_creation(self):
        # Create an Education instance
        education = Education.objects.create(
            user=self.user,
            qualification='Bachelor of Science',
            institution_name='Example University',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2023, 1, 1)
        )
        self.assertEqual(education.user, self.user)
        self.assertEqual(education.qualification, 'Bachelor of Science')
        self.assertEqual(education.institution_name, 'Example University')
        self.assertEqual(education.start_date, datetime.date(2020, 1, 1))
        self.assertEqual(education.end_date, datetime.date(2023, 1, 1))
        self.assertEqual(str(education), 'Bachelor of Science from Example University')

    def test_education_update(self):
        # Create and update an Education instance
        education = Education.objects.create(
            user=self.user,
            qualification='Bachelor of Science',
            institution_name='Example University',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2023, 1, 1)
        )
        education.qualification = 'Master of Science'
        education.save()

        # Retrieve and check updated value
        updated_education = Education.objects.get(id=education.id)
        self.assertEqual(updated_education.qualification, 'Master of Science')

    def test_education_delete(self):
        # Create and delete an Education instance
        education = Education.objects.create(
            user=self.user,
            qualification='Bachelor of Science',
            institution_name='Example University',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2023, 1, 1)
        )
        education_id = education.id
        education.delete()

        # Ensure the instance is deleted
        with self.assertRaises(Education.DoesNotExist):
            Education.objects.get(id=education_id)
