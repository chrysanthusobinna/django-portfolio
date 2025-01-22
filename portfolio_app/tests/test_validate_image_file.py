from django.test import TestCase
from django.http import HttpRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio_app.utils import validate_image_file  # Adjust import based on your project structure

class ValidateImageFileTests(TestCase):
    def setUp(self):
        # Create a request object for testing
        self.request = HttpRequest()

    def test_valid_image_file(self):
        # Simulate a valid image file (e.g., .jpg)
        self.request.FILES['profile_photo'] = SimpleUploadedFile("image.jpg", b"image content", content_type="image/jpeg")
        
        # Test the function with a valid file type
        is_valid, error_message = validate_image_file(self.request, 'profile_photo', 'Profile Photo')
        
        # Check if the file is valid
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)

    def test_invalid_image_file_extension(self):
        # Simulate an invalid image file (e.g., .txt)
        self.request.FILES['profile_photo'] = SimpleUploadedFile("file.txt", b"file content", content_type="text/plain")
        
        # Test the function with an invalid file type
        is_valid, error_message = validate_image_file(self.request, 'profile_photo', 'Profile Photo')
        
        # Check if the file is invalid
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "Invalid file type for Profile Photo. Only jpg, jpeg, png, gif files are allowed.")

    def test_missing_file(self):
        # Test when no file is uploaded
        is_valid, error_message = validate_image_file(self.request, 'profile_photo', 'Profile Photo')
        
        # Check if the validation passes (since there's no file)
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
