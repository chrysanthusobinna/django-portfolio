from django.test import TestCase
from portfolio_app.cv_parser import CVParser


class CVParserContactExtractionTests(TestCase):
    """Tests for CVParser contact information extraction"""

    def setUp(self):
        self.parser = CVParser()
        self.sample_cv_text = """
        John Doe
        Software Engineer

        Contact:
        Email: john.doe@example.com
        Phone: +1 (555) 123-4567
        LinkedIn: https://linkedin.com/in/johndoe

        Summary:
        Experienced software engineer with 5+ years of experience in full-stack development,
        specializing in Python, Django, and React. Passionate about building scalable
        web applications and leading development teams.

        Work Experience:
        Senior Software Engineer at Tech Corp
        June 2020 - Present
        Led development of enterprise web applications using Django and React.
        Managed a team of 5 developers and implemented CI/CD pipelines.

        Software Developer at StartupXYZ
        January 2018 - May 2020
        Developed RESTful APIs and responsive front-end interfaces.
        Worked with Python, JavaScript, and PostgreSQL.

        Education:
        Bachelor of Science in Computer Science
        University of Technology
        September 2014 - May 2018

        Certifications:
        AWS Certified Solutions Architect
        Issued by Amazon Web Services
        March 2021

        Django Developer Certification
        Issued by Django Software Foundation
        November 2019

        Projects:
        E-Commerce Platform
        Full-featured online shopping platform built with Django and React.
        Includes user authentication, payment processing, and admin dashboard.
        https://github.com/johndoe/ecommerce

        Task Management App
        Collaborative project management tool with real-time updates.
        Built using Django Channels and WebSocket technology.
        """

    def test_extract_email(self):
        contact = self.parser.extract_contact_info(self.sample_cv_text)
        self.assertEqual(contact.get('email'), 'john.doe@example.com')

    def test_extract_phone(self):
        contact = self.parser.extract_contact_info(self.sample_cv_text)
        self.assertEqual(contact.get('phone'), '+1 (555) 123-4567')

    def test_extract_linkedin(self):
        contact = self.parser.extract_contact_info(self.sample_cv_text)
        self.assertEqual(contact.get('linkedin'), 'https://linkedin.com/in/johndoe')

    def test_no_contact_info(self):
        contact = self.parser.extract_contact_info('No contact info here.')
        self.assertIsNone(contact.get('email'))
        self.assertIsNone(contact.get('phone'))
        self.assertIsNone(contact.get('linkedin'))


class CVParserSummaryExtractionTests(TestCase):
    """Tests for CVParser about/summary extraction"""

    def setUp(self):
        self.parser = CVParser()

    def test_extract_summary(self):
        text = "Dedicated software engineer specializing in Python, Django, and React with a passion for building scalable web applications.\nEducation\nBSc Computer Science"
        about = self.parser.extract_about_summary(text)
        self.assertIsNotNone(about)
        self.assertIn('software engineer', about.lower())

    def test_no_summary(self):
        about = self.parser.extract_about_summary('Short text')
        self.assertIsNone(about)
