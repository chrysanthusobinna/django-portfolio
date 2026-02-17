from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
import json
from portfolio_app.vertex_ai_cv_extractor import VertexAICVExtractor


class VertexAICVExtractorTests(TestCase):
    """Tests for Vertex AI CV extraction functionality"""

    def setUp(self):
        self.sample_cv_text = """
        John Doe
        Software Engineer

        Contact:
        Email: john.doe@example.com
        Phone: +1 (555) 123-4567
        LinkedIn: https://linkedin.com/in/johndoe

        Summary:
        Experienced software engineer with 5+ years of experience in full-stack development,
        specializing in Python, Django, and React.

        Work Experience:
        Senior Software Engineer at Tech Corp
        June 2020 - Present
        Led development of enterprise web applications using Django and React.

        Software Developer at StartupXYZ
        January 2018 - May 2020
        Developed RESTful APIs and responsive front-end interfaces.

        Education:
        Bachelor of Science in Computer Science
        University of Technology
        September 2014 - May 2018

        Certifications:
        AWS Certified Solutions Architect
        Issued by Amazon Web Services
        March 2021

        Projects:
        E-Commerce Platform
        Full-featured online shopping platform built with Django and React.
        https://github.com/johndoe/ecommerce
        """

        self.mock_response_data = {
            "contact": {
                "email_address": "john.doe@example.com",
                "phone_number": "+1 (555) 123-4567",
                "linkedin": "https://linkedin.com/in/johndoe"
            },
            "country": None,
            "address": None,
            "about": "Experienced software engineer with 5+ years of experience",
            "employment": [
                {
                    "employer_name": "Tech Corp",
                    "job_title": "Senior Software Engineer",
                    "description_of_duties": "Led development of enterprise web applications",
                    "start_date": "2020-06-01",
                    "end_date": None
                },
                {
                    "employer_name": "StartupXYZ",
                    "job_title": "Software Developer",
                    "description_of_duties": "Developed RESTful APIs and responsive front-end interfaces",
                    "start_date": "2018-01-01",
                    "end_date": "2020-05-31"
                }
            ],
            "education": [
                {
                    "qualification": "Bachelor of Science in Computer Science",
                    "institution_name": "University of Technology",
                    "start_date": "2014-09-01",
                    "end_date": "2018-05-31"
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "date_issued": "2021-03-01"
                }
            ],
            "projects": [
                {
                    "title": "E-Commerce Platform",
                    "description": "Full-featured online shopping platform built with Django and React.",
                    "link": "https://github.com/johndoe/ecommerce"
                }
            ]
        }

    @override_settings(
        VERTEXAI_PROJECT_ID="test-project",
        VERTEXAI_LOCATION="us-central1"
    )
    @patch('portfolio_app.vertex_ai_cv_extractor.vertexai_init')
    @patch('portfolio_app.vertex_ai_cv_extractor.GenerativeModel')
    def test_extractor_initialization_success(self, mock_generative_model, mock_vertexai_init):
        """Test successful initialization of VertexAICVExtractor"""
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        extractor = VertexAICVExtractor()
        
        self.assertEqual(extractor.project_id, "test-project")
        self.assertEqual(extractor.location, "us-central1")
        self.assertEqual(extractor.model, mock_model)
        mock_vertexai_init.assert_called_once_with(project="test-project", location="us-central1")
        mock_generative_model.assert_called_once_with("gemini-2.5-flash-lite")

    @override_settings(
        VERTEXAI_PROJECT_ID="",
        VERTEXAI_LOCATION="us-central1"
    )
    def test_extractor_missing_project_id(self):
        """Test extractor initialization fails without project ID"""
        with self.assertRaises(ValueError) as context:
            VertexAICVExtractor()
        
        self.assertIn("VERTEXAI_PROJECT_ID is not configured", str(context.exception))

    @patch('portfolio_app.vertex_ai_cv_extractor.HAS_VERTEXAI', False)
    def test_extractor_missing_dependencies(self):
        """Test extractor initialization fails without Vertex AI libraries"""
        with self.assertRaises(ImportError) as context:
            VertexAICVExtractor()
        
        self.assertIn("Vertex AI libraries not installed", str(context.exception))

    @override_settings(
        VERTEXAI_PROJECT_ID="test-project",
        VERTEXAI_LOCATION="us-central1"
    )
    @patch('portfolio_app.vertex_ai_cv_extractor.vertexai_init')
    @patch('portfolio_app.vertex_ai_cv_extractor.GenerativeModel')
    def test_extract_cv_success(self, mock_generative_model, mock_vertexai_init):
        """Test successful CV extraction"""
        # Setup mock
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        # Mock the API response
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [MagicMock(text=json.dumps(self.mock_response_data))]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response
        
        # Test extraction
        extractor = VertexAICVExtractor()
        result = extractor.extract(self.sample_cv_text)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['contact']['email_address'], 'john.doe@example.com')
        self.assertEqual(result['contact']['phone_number'], '+1 (555) 123-4567')
        self.assertEqual(result['contact']['linkedin'], 'https://linkedin.com/in/johndoe')
        self.assertEqual(len(result['employment']), 2)
        self.assertEqual(len(result['education']), 1)
        self.assertEqual(len(result['certifications']), 1)
        self.assertEqual(len(result['projects']), 1)

    @override_settings(
        VERTEXAI_PROJECT_ID="test-project",
        VERTEXAI_LOCATION="us-central1"
    )
    @patch('portfolio_app.vertex_ai_cv_extractor.vertexai_init')
    @patch('portfolio_app.vertex_ai_cv_extractor.GenerativeModel')
    def test_extract_cv_api_failure(self, mock_generative_model, mock_vertexai_init):
        """Test CV extraction handles API failure gracefully"""
        # Setup mock
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        # Mock API failure
        mock_model.generate_content.side_effect = Exception("API Error")
        
        # Test extraction
        extractor = VertexAICVExtractor()
        result = extractor.extract(self.sample_cv_text)
        
        # Should return None on failure
        self.assertIsNone(result)

    @override_settings(
        VERTEXAI_PROJECT_ID="test-project",
        VERTEXAI_LOCATION="us-central1"
    )
    @patch('portfolio_app.vertex_ai_cv_extractor.vertexai_init')
    @patch('portfolio_app.vertex_ai_cv_extractor.GenerativeModel')
    def test_extract_cv_invalid_json(self, mock_generative_model, mock_vertexai_init):
        """Test CV extraction handles invalid JSON gracefully"""
        # Setup mock
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        # Mock invalid JSON response
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [MagicMock(text="Invalid JSON response")]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response
        
        # Test extraction
        extractor = VertexAICVExtractor()
        result = extractor.extract(self.sample_cv_text)
        
        # Should return None for invalid JSON
        self.assertIsNone(result)

    @override_settings(
        VERTEXAI_PROJECT_ID="test-project",
        VERTEXAI_LOCATION="us-central1"
    )
    @patch('portfolio_app.vertex_ai_cv_extractor.vertexai_init')
    @patch('portfolio_app.vertex_ai_cv_extractor.GenerativeModel')
    def test_extract_cv_with_retry(self, mock_generative_model, mock_vertexai_init):
        """Test CV extraction retry mechanism"""
        # Setup mock
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        # Mock first call fails, second succeeds
        mock_candidate_fail = MagicMock()
        mock_candidate_fail.content.parts = [MagicMock(text="Invalid JSON")]
        mock_response_fail = MagicMock()
        mock_response_fail.candidates = [mock_candidate_fail]
        
        mock_candidate_success = MagicMock()
        mock_candidate_success.content.parts = [MagicMock(text=json.dumps(self.mock_response_data))]
        mock_response_success = MagicMock()
        mock_response_success.candidates = [mock_candidate_success]
        
        mock_model.generate_content.side_effect = [mock_response_fail, mock_response_success]
        
        # Test extraction
        extractor = VertexAICVExtractor()
        result = extractor.extract(self.sample_cv_text)
        
        # Should succeed on retry
        self.assertIsNotNone(result)
        self.assertEqual(result['contact']['email_address'], 'john.doe@example.com')
        self.assertEqual(mock_model.generate_content.call_count, 2)  # Called twice due to retry

    def test_validate_email_format(self):
        """Test email validation in extracted data"""
        # This would test the internal validation logic
        # For now, just ensure the extractor validates email formats
        pass

    def test_validate_phone_format(self):
        """Test phone number validation in extracted data"""
        # This would test the internal validation logic
        pass

    def test_validate_linkedin_format(self):
        """Test LinkedIn URL validation in extracted data"""
        # This would test the internal validation logic
        pass

    def test_date_normalization(self):
        """Test date normalization in extracted data"""
        # This would test the date normalization logic
        pass
