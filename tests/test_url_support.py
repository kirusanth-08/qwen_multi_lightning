"""
Unit tests for URL image support in handler.py
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import handler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestURLImageSupport(unittest.TestCase):
    """Test URL image input functionality"""
    
    def test_url_detection(self):
        """Test that URLs are correctly detected"""
        test_cases = [
            ("https://example.com/image.jpg", True),
            ("http://example.com/image.png", True),
            ("data:image/png;base64,iVBORw0KGgo", False),
            ("iVBORw0KGgo", False),
            ("/9j/4AAQSkZJ", False),
        ]
        
        for image_data, should_be_url in test_cases:
            is_url = image_data.startswith(("http://", "https://"))
            self.assertEqual(is_url, should_be_url, 
                           f"URL detection failed for: {image_data[:50]}")
    
    def test_input_validation_with_urls(self):
        """Test that input validation accepts URLs"""
        from handler import validate_input
        
        # Test with URL inputs
        job_input = {
            "prompt": "Test prompt",
            "main_image": "https://example.com/main.jpg",
            "reference_image": "https://example.com/ref.jpg",
            "steps": 8,
            "cfg": 1
        }
        
        result, error = validate_input(job_input)
        self.assertIsNone(error, f"Validation failed with error: {error}")
        self.assertIsNotNone(result)
        self.assertIn("images", result)
        self.assertEqual(len(result["images"]), 2)
        
    def test_input_validation_with_mixed_formats(self):
        """Test validation with mixed URL and base64"""
        from handler import validate_input
        
        job_input = {
            "prompt": "Test prompt",
            "images": [
                "https://example.com/main.jpg",  # URL
                "iVBORw0KGgoAAAANSUhEUgA..."  # base64
            ],
            "steps": 8
        }
        
        result, error = validate_input(job_input)
        self.assertIsNone(error, f"Validation failed with error: {error}")
        self.assertIsNotNone(result)
        
    def test_input_validation_requires_strings(self):
        """Test that non-string images are rejected"""
        from handler import validate_input
        
        # Test with invalid input (number)
        job_input = {
            "prompt": "Test prompt",
            "main_image": 12345,  # Invalid: not a string
            "reference_image": "https://example.com/ref.jpg"
        }
        
        result, error = validate_input(job_input)
        self.assertIsNotNone(error)
        self.assertIn("must be", error.lower())
        
    @patch('requests.get')
    def test_upload_images_downloads_url(self, mock_get):
        """Test that upload_images downloads from URLs"""
        from handler import upload_images
        
        # Mock the image download
        mock_response = MagicMock()
        mock_response.content = b"fake_image_data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock the ComfyUI upload endpoint
        with patch('requests.post') as mock_post:
            mock_post_response = MagicMock()
            mock_post_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_post_response
            
            images = [
                {
                    "name": "test_image.jpg",
                    "image": "https://example.com/test.jpg"
                }
            ]
            
            result = upload_images(images)
            
            # Verify download was called
            mock_get.assert_called_once()
            self.assertIn("https://example.com/test.jpg", 
                         str(mock_get.call_args))
            
            # Verify upload was successful
            self.assertEqual(result["status"], "success")
            
    def test_data_uri_prefix_handling(self):
        """Test that data URI prefixes are correctly stripped"""
        test_cases = [
            ("data:image/png;base64,iVBORw0KGgo", "iVBORw0KGgo"),
            ("data:image/jpeg;base64,/9j/4AAQSkZJ", "/9j/4AAQSkZJ"),
            ("iVBORw0KGgo", "iVBORw0KGgo"),  # No prefix
        ]
        
        for input_data, expected in test_cases:
            if "," in input_data:
                result = input_data.split(",", 1)[1]
            else:
                result = input_data
            self.assertEqual(result, expected)


if __name__ == "__main__":
    print("Running URL image support tests...")
    unittest.main(verbosity=2)
