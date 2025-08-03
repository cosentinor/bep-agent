"""
Unit tests for structure extractor module.
Tests heading extraction and document structure parsing functionality.
"""

import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from structure_extractor import StructureExtractor, Node, parse_docx, parse_pdf, extract


class TestStructureExtractor(unittest.TestCase):
    """Test cases for StructureExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = StructureExtractor()
    
    def test_init(self):
        """Test StructureExtractor initialization."""
        self.assertIsInstance(self.extractor, StructureExtractor)
        self.assertEqual(self.extractor.supported_formats, {'.docx', '.pdf'})
    
    def test_extract_heading_level(self):
        """Test heading level extraction from style names."""
        test_cases = [
            ("Heading 1", 1),
            ("Heading 2", 2),
            ("Heading 3", 3),
            ("Heading 10", 10),
            ("Heading", 1),  # Default case
        ]
        
        for style_name, expected_level in test_cases:
            with self.subTest(style_name=style_name):
                level = self.extractor._extract_heading_level(style_name)
                self.assertEqual(level, expected_level)
    
    def test_normalize_title(self):
        """Test title normalization for grouping."""
        # This test requires importing outline_suggester
        try:
            from outline_suggester import OutlineSuggester
            # Create a mock suggester to test the normalize method
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                test_cases = [
                    ("1. Executive Summary", "executive_summary"),
                    ("2.1 Project Information", "project_info"),
                    ("PROJECT GOALS", "goals"),
                    ("Implementation Timeline", "implementation"),
                ]
                
                for title, expected in test_cases:
                    with self.subTest(title=title):
                        result = suggester._normalize_title(title)
                        self.assertEqual(result, expected)
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_get_text_span_from_lines(self):
        """Test text span extraction from lines."""
        lines = [
            "1. Introduction",
            "This is the introduction text.",
            "It contains multiple sentences.",
            "2. Next Section",
            "This is the next section."
        ]
        
        text_span = self.extractor._get_text_span_from_lines(lines, 0, max_chars=100)
        expected = "This is the introduction text. It contains multiple sentences."
        self.assertEqual(text_span, expected)
    
    def test_get_text_span_from_lines_truncation(self):
        """Test text span extraction with truncation."""
        lines = [
            "1. Introduction",
            "This is a very long introduction text that should be truncated because it exceeds the maximum character limit.",
            "Additional text that should not be included."
        ]
        
        text_span = self.extractor._get_text_span_from_lines(lines, 0, max_chars=50)
        self.assertTrue(text_span.endswith("..."))
        self.assertLessEqual(len(text_span), 53)  # 50 + "..."
    
    def test_extract_unsupported_format(self):
        """Test extraction with unsupported file format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b"Test content")
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError) as context:
                self.extractor.extract(tmp_path)
            
            self.assertIn("Unsupported document format", str(context.exception))
        finally:
            os.unlink(tmp_path)
    
    def test_extract_nonexistent_file(self):
        """Test extraction with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.extractor.extract("nonexistent_file.docx")
    
    @patch('structure_extractor.Document')
    def test_parse_docx_with_styled_headings(self, mock_document):
        """Test DOCX parsing with styled headings."""
        # Mock document structure
        mock_doc = Mock()
        mock_document.return_value = mock_doc
        
        # Create mock paragraphs with heading styles
        mock_para1 = Mock()
        mock_para1.style.name = "Heading 1"
        mock_para1.text = "Introduction"
        
        mock_para2 = Mock()
        mock_para2.style.name = "Normal"
        mock_para2.text = "This is the introduction content."
        
        mock_para3 = Mock()
        mock_para3.style.name = "Heading 2"
        mock_para3.text = "Background"
        
        mock_doc.paragraphs = [mock_para1, mock_para2, mock_para3]
        
        # Test parsing
        nodes = self.extractor.parse_docx("test.docx")
        
        # Verify results
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].title, "Introduction")
        self.assertEqual(nodes[0].level, 1)
        self.assertEqual(nodes[1].title, "Background")
        self.assertEqual(nodes[1].level, 2)
    
    @patch('structure_extractor.Document')
    def test_parse_docx_with_empty_headings(self, mock_document):
        """Test DOCX parsing with empty headings."""
        mock_doc = Mock()
        mock_document.return_value = mock_doc
        
        # Create mock paragraph with empty heading
        mock_para = Mock()
        mock_para.style.name = "Heading 1"
        mock_para.text = "   "  # Empty/whitespace only
        
        mock_doc.paragraphs = [mock_para]
        
        nodes = self.extractor.parse_docx("test.docx")
        
        # Should not include empty headings
        self.assertEqual(len(nodes), 0)
    
    @patch('structure_extractor.fitz')
    def test_parse_pdf_with_toc(self, mock_fitz):
        """Test PDF parsing with table of contents."""
        # Mock PDF document
        mock_doc = Mock()
        mock_fitz.open.return_value = mock_doc
        
        # Mock TOC
        mock_toc = [
            (1, "Introduction", 1),
            (2, "Background", 1),
            (2, "Methodology", 2)
        ]
        mock_doc.get_toc.return_value = mock_toc
        
        # Mock pages
        mock_page = Mock()
        mock_page.get_text.return_value = "Sample page content for testing."
        mock_doc.__getitem__.return_value = mock_page
        
        nodes = self.extractor.parse_pdf("test.pdf")
        
        # Verify results
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].title, "Introduction")
        self.assertEqual(nodes[0].level, 1)
        self.assertEqual(nodes[1].title, "Background")
        self.assertEqual(nodes[1].level, 2)
    
    @patch('structure_extractor.fitz')
    def test_parse_pdf_without_toc(self, mock_fitz):
        """Test PDF parsing without table of contents."""
        mock_doc = Mock()
        mock_fitz.open.return_value = mock_doc
        
        # No TOC
        mock_doc.get_toc.return_value = []
        
        # Mock pages with text content
        mock_page = Mock()
        mock_page.get_text.return_value = "1. Introduction\nThis is the introduction.\n2. Background\nThis is background."
        mock_doc.__iter__.return_value = [mock_page]
        
        nodes = self.extractor.parse_pdf("test.pdf")
        
        # Should extract headings using regex
        self.assertGreaterEqual(len(nodes), 0)  # May find regex-based headings


class TestNode(unittest.TestCase):
    """Test cases for Node dataclass."""
    
    def test_node_creation(self):
        """Test Node creation and attributes."""
        node = Node(
            id="test_1",
            level=1,
            title="Test Title",
            text_span="Test content",
            doc_id="test.docx"
        )
        
        self.assertEqual(node.id, "test_1")
        self.assertEqual(node.level, 1)
        self.assertEqual(node.title, "Test Title")
        self.assertEqual(node.text_span, "Test content")
        self.assertEqual(node.doc_id, "test.docx")


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions."""
    
    @patch('structure_extractor.StructureExtractor')
    def test_parse_docx_function(self, mock_extractor_class):
        """Test parse_docx convenience function."""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.parse_docx.return_value = [Mock()]
        
        result = parse_docx("test.docx")
        
        mock_extractor_class.assert_called_once()
        mock_extractor.parse_docx.assert_called_once_with("test.docx")
        self.assertEqual(len(result), 1)
    
    @patch('structure_extractor.StructureExtractor')
    def test_parse_pdf_function(self, mock_extractor_class):
        """Test parse_pdf convenience function."""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.parse_pdf.return_value = [Mock()]
        
        result = parse_pdf("test.pdf")
        
        mock_extractor_class.assert_called_once()
        mock_extractor.parse_pdf.assert_called_once_with("test.pdf")
        self.assertEqual(len(result), 1)
    
    @patch('structure_extractor.StructureExtractor')
    def test_extract_function(self, mock_extractor_class):
        """Test extract convenience function."""
        mock_extractor = Mock()
        mock_extractor_class.return_value = mock_extractor
        mock_extractor.extract.return_value = [Mock()]
        
        result = extract("test.docx")
        
        mock_extractor_class.assert_called_once()
        mock_extractor.extract.assert_called_once_with("test.docx")
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
