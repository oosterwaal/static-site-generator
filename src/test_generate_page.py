import unittest
import os
import tempfile
import shutil
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_page import generate_page

class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.content_dir = os.path.join(self.test_dir, "content")
        self.public_dir = os.path.join(self.test_dir, "public")
        os.makedirs(self.content_dir)
        os.makedirs(self.public_dir)
        
        # Create test markdown file
        self.markdown_content = """# Test Page

This is a **test** page with some content.

> This is a quote

## Subheading

- Item 1
- Item 2
"""
        self.markdown_path = os.path.join(self.content_dir, "test.md")
        with open(self.markdown_path, 'w') as f:
            f.write(self.markdown_content)
        
        # Create test template
        self.template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ Title }}</title>
</head>
<body>
    <div>{{ Content }}</div>
</body>
</html>"""
        self.template_path = os.path.join(self.test_dir, "template.html")
        with open(self.template_path, 'w') as f:
            f.write(self.template_content)
        
        self.output_path = os.path.join(self.public_dir, "test.html")

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    def test_generate_page(self):
        # Test the generate_page function
        generate_page(self.markdown_path, self.template_path, self.output_path)
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(self.output_path))
        
        # Read and check the output
        with open(self.output_path, 'r') as f:
            html_content = f.read()
        
        # Check that title was replaced
        self.assertIn("<title>Test Page</title>", html_content)
        
        # Check that content was replaced and contains expected HTML
        self.assertIn("<h1>Test Page</h1>", html_content)
        self.assertIn("<b>test</b>", html_content)
        self.assertIn("<blockquote>This is a quote</blockquote>", html_content)
        self.assertIn("<h2>Subheading</h2>", html_content)
        self.assertIn("<ul>", html_content)
        self.assertIn("<li>Item 1</li>", html_content)
        self.assertIn("<li>Item 2</li>", html_content)

    def test_generate_page_creates_directories(self):
        # Test that generate_page creates necessary directories
        nested_output_path = os.path.join(self.public_dir, "nested", "deep", "test.html")
        
        generate_page(self.markdown_path, self.template_path, nested_output_path)
        
        # Check that the nested directories were created
        self.assertTrue(os.path.exists(nested_output_path))

if __name__ == "__main__":
    unittest.main()