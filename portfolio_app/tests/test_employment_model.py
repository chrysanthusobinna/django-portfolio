from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import Employment
import datetime

class EmploymentModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_employment_creation(self):
        # Create an Employment instance
        employment = Employment.objects.create(
            user=self.user,
            employer_name='Tech Corp',
            job_title='Software Engineer',
            description_of_duties='Developed software applications.',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2023, 1, 1)
        )
        self.assertEqual(employment.user, self.user)
        self.assertEqual(employment.employer_name, 'Tech Corp')
        self.assertEqual(employment.job_title, 'Software Engineer')
        self.assertEqual(employment.description_of_duties, 'Developed software applications.')
        self.assertEqual(employment.start_date, datetime.date(2020, 1, 1))
        self.assertEqual(employment.end_date, datetime.date(2023, 1, 1))
        self.assertEqual(str(employment), 'Software Engineer at Tech Corp')

    def test_employment_update(self):
        # Create and update an Employment instance
        employment = Employment.objects.create(
            user=self.user,
            employer_name='Tech Corp',
            job_title='Software Engineer',
            description_of_duties='Developed software applications.',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2023, 1, 1)
        )
        employment.job_title = 'Senior Software Engineer'
        employment.save()

        # Retrieve and check updated value
        updated_employment = Employment.objects.get(id=employment.id)
        self.assertEqual(updated_employment.job_title, 'Senior Software Engineer')

    def test_employment_delete(self):
        # Create and delete an Employment instance
        employment = Employment.objects.create(
            user=self.user,
            employer_name='Tech Corp',
            job_title='Software Engineer',
            description_of_duties='Developed software applications.',
            start_date=datetime.date(2020, 1, 1),
            end_date=datetime.date(2023, 1, 1)
        )
        employment_id = employment.id
        employment.delete()

        # Ensure the instance is deleted
        with self.assertRaises(Employment.DoesNotExist):
            Employment.objects.get(id=employment_id)
