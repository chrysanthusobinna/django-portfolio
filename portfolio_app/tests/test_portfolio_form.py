from django.test import TestCase
from django.contrib.auth.models import User
from portfolio_app.forms import PortfolioForm
from portfolio_app.models import Portfolio

class PortfolioFormTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_portfolio_form_valid(self):
        # Valid form data
        form_data = {
            'title': 'My Portfolio',
            'description': 'A description of my portfolio.',
            'link': 'https://example.com',
            'portfolio_photo': None  # Assuming no photo is provided initially
        }
        form = PortfolioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_portfolio_form_invalid_missing_title(self):
        # Invalid form data (missing title)
        form_data = {
            'description': 'A description of my portfolio.',
            'link': 'https://example.com',
            'portfolio_photo': None  # Assuming no photo is provided initially
        }
        form = PortfolioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_portfolio_form_invalid_missing_description(self):
        # Invalid form data (missing description)
        form_data = {
            'title': 'My Portfolio',
            'link': 'https://example.com',
            'portfolio_photo': None  # Assuming no photo is provided initially
        }
        form = PortfolioForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_portfolio_form_save(self):
        # Test saving valid form data to the database
        form_data = {
            'title': 'My Portfolio',
            'description': 'A description of my portfolio.',
            'link': 'https://example.com',
            'portfolio_photo': None  # Assuming no photo is provided initially
        }
        form = PortfolioForm(data=form_data)
        self.assertTrue(form.is_valid())
        portfolio = form.save(commit=False)
        portfolio.user = self.user  # Associate the portfolio with the test user
        portfolio.save()

        # Verify the data is saved correctly
        saved_portfolio = Portfolio.objects.get(id=portfolio.id)
        self.assertEqual(saved_portfolio.title, form_data['title'])
        self.assertEqual(saved_portfolio.description, form_data['description'])
        self.assertEqual(saved_portfolio.link, form_data['link'])
