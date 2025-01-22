from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.models import Certification
import datetime

class CertificationModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_certification_creation(self):
        # Create a Certification instance
        certification = Certification.objects.create(
            user=self.user,
            name='Certified Python Developer',
            issuer='Python Institute',
            date_issued=datetime.date(2023, 1, 1)
        )
        self.assertEqual(certification.user, self.user)
        self.assertEqual(certification.name, 'Certified Python Developer')
        self.assertEqual(certification.issuer, 'Python Institute')
        self.assertEqual(certification.date_issued, datetime.date(2023, 1, 1))
        self.assertEqual(str(certification), 'Certified Python Developer by Python Institute')

    def test_certification_update(self):
        # Create and update a Certification instance
        certification = Certification.objects.create(
            user=self.user,
            name='Certified Python Developer',
            issuer='Python Institute',
            date_issued=datetime.date(2023, 1, 1)
        )
        certification.name = 'Advanced Python Developer'
        certification.save()

        # Retrieve and check updated value
        updated_certification = Certification.objects.get(id=certification.id)
        self.assertEqual(updated_certification.name, 'Advanced Python Developer')

    def test_certification_delete(self):
        # Create and delete a Certification instance
        certification = Certification.objects.create(
            user=self.user,
            name='Certified Python Developer',
            issuer='Python Institute',
            date_issued=datetime.date(2023, 1, 1)
        )
        certification_id = certification.id
        certification.delete()

        # Ensure the instance is deleted
        with self.assertRaises(Certification.DoesNotExist):
            Certification.objects.get(id=certification_id)
