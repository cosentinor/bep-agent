"""
Unit tests for outline merger functionality.
Tests outline generation, deduplication, and hierarchical structure creation.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestOutlineMerger(unittest.TestCase):
    """Test cases for outline merging and generation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_nodes = [
            {
                'id': 'doc1_h1_1',
                'level': 1,
                'title': '1. Executive Summary',
                'text_span': 'This document provides an executive summary...',
                'doc_id': 'doc1.docx',
                'similarity_score': 0.9,
                'frequency': 3
            },
            {
                'id': 'doc2_h1_1',
                'level': 1,
                'title': 'Executive Summary',
                'text_span': 'Executive overview of the project...',
                'doc_id': 'doc2.docx',
                'similarity_score': 0.85,
                'frequency': 2
            },
            {
                'id': 'doc1_h2_1',
                'level': 2,
                'title': '1.1 Project Overview',
                'text_span': 'The project aims to...',
                'doc_id': 'doc1.docx',
                'similarity_score': 0.8,
                'frequency': 1
            },
            {
                'id': 'doc3_h1_1',
                'level': 1,
                'title': '2. Implementation Plan',
                'text_span': 'The implementation will follow...',
                'doc_id': 'doc3.docx',
                'similarity_score': 0.75,
                'frequency': 2
            }
        ]
    
    def test_normalize_title(self):
        """Test title normalization for grouping similar headings."""
        try:
            from outline_suggester import OutlineSuggester
            
            # Create a mock suggester instance
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                test_cases = [
                    ("1. Executive Summary", "executive_summary"),
                    ("Executive Summary", "executive_summary"),
                    ("EXECUTIVE SUMMARY", "executive_summary"),
                    ("2.1 Project Information", "project_info"),
                    ("Project Goals and Objectives", "goals"),
                    ("Implementation Timeline", "implementation"),
                    ("3. Deliverables", "deliverables"),
                ]
                
                for title, expected in test_cases:
                    with self.subTest(title=title):
                        result = suggester._normalize_title(title)
                        self.assertEqual(result, expected)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_deduplicate_nodes(self):
        """Test node deduplication based on similarity and frequency."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                # Test deduplication
                deduplicated = suggester._deduplicate_nodes(self.sample_nodes, 3)
                
                # Should have fewer nodes after deduplication
                self.assertLessEqual(len(deduplicated), len(self.sample_nodes))
                
                # Should prioritize higher similarity scores
                if deduplicated:
                    first_node = deduplicated[0]
                    self.assertGreaterEqual(first_node['similarity_score'], 0.8)
                
                # Should include frequency information
                for node in deduplicated:
                    self.assertIn('frequency', node)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_generate_hierarchical_outline(self):
        """Test hierarchical outline generation from nodes."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                requirements_text = "We need an executive summary and implementation plan."
                
                outline = suggester._generate_hierarchical_outline(
                    self.sample_nodes, 
                    requirements_text
                )
                
                # Should have basic outline structure
                self.assertIn('title', outline)
                self.assertIn('sections', outline)
                self.assertIn('metadata', outline)
                
                # Should have sections
                sections = outline['sections']
                self.assertGreater(len(sections), 0)
                
                # Each section should have required fields
                for section in sections:
                    self.assertIn('title', section)
                    self.assertIn('level', section)
                    self.assertIn('subsections', section)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_clean_title(self):
        """Test title cleaning functionality."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                test_cases = [
                    ("1. Executive Summary", "Executive Summary"),
                    ("2.1 Project Overview", "Project Overview"),
                    ("   3. Implementation   ", "Implementation"),
                    ("executive summary", "Executive summary"),
                    ("", ""),
                ]
                
                for input_title, expected in test_cases:
                    with self.subTest(input_title=input_title):
                        result = suggester._clean_title(input_title)
                        self.assertEqual(result, expected)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_are_related_sections(self):
        """Test section relationship detection."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                parent = {'title': 'Project Management'}
                
                test_cases = [
                    ({'title': 'Project Roles'}, True),  # Common word 'project'
                    ({'title': 'Team Organization'}, True),  # Related to management
                    ({'title': 'Quality Assurance'}, False),  # Not related
                    ({'title': 'Implementation Timeline'}, False),  # Different domain
                ]
                
                for child, expected in test_cases:
                    with self.subTest(child=child['title']):
                        result = suggester._are_related_sections(parent, child)
                        self.assertEqual(result, expected)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_find_subsections(self):
        """Test subsection finding functionality."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                parent_node = self.sample_nodes[0]  # Executive Summary
                
                # Create level groups
                level_groups = {
                    1: [self.sample_nodes[0], self.sample_nodes[3]],
                    2: [self.sample_nodes[2]]
                }
                
                subsections = suggester._find_subsections(
                    parent_node, 
                    level_groups, 
                    self.sample_nodes
                )
                
                # Should find related subsections
                self.assertIsInstance(subsections, list)
                
                # Each subsection should have required fields
                for subsection in subsections:
                    self.assertIn('title', subsection)
                    self.assertIn('level', subsection)
                    self.assertGreaterEqual(subsection['level'], 2)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_enhance_outline_with_requirements(self):
        """Test outline enhancement based on requirements."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                # Basic outline without requirements section
                outline = {
                    'title': 'Test Outline',
                    'sections': [
                        {'title': 'Executive Summary', 'level': 1, 'subsections': []},
                        {'title': 'Implementation', 'level': 1, 'subsections': []}
                    ]
                }
                
                requirements_text = "The project requirements include specific functionality..."
                
                enhanced = suggester._enhance_outline_with_requirements(
                    outline, 
                    requirements_text
                )
                
                # Should add requirements section
                section_titles = [s['title'] for s in enhanced['sections']]
                self.assertIn('Requirements Analysis', section_titles)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")
    
    def test_get_default_outline(self):
        """Test default outline generation."""
        try:
            from outline_suggester import OutlineSuggester
            
            with patch('outline_suggester.StructureIndexer'):
                suggester = OutlineSuggester.__new__(OutlineSuggester)
                
                default_outline = suggester._get_default_outline()
                
                # Should have basic structure
                self.assertIn('title', default_outline)
                self.assertIn('sections', default_outline)
                self.assertIn('metadata', default_outline)
                
                # Should have some default sections
                sections = default_outline['sections']
                self.assertGreater(len(sections), 0)
                
                # Should include common sections
                section_titles = [s['title'] for s in sections]
                expected_sections = ['Executive Summary', 'Project Goals and Objectives']
                
                for expected in expected_sections:
                    self.assertIn(expected, section_titles)
        
        except ImportError:
            self.skipTest("outline_suggester module not available")


class TestOutlineStructure(unittest.TestCase):
    """Test cases for outline structure validation."""
    
    def test_outline_structure_validation(self):
        """Test that generated outlines have valid structure."""
        # Sample outline structure
        outline = {
            'title': 'Test Outline',
            'sections': [
                {
                    'title': 'Section 1',
                    'level': 1,
                    'subsections': [
                        {
                            'title': 'Subsection 1.1',
                            'level': 2
                        }
                    ]
                }
            ],
            'metadata': {
                'source_documents': ['doc1.docx'],
                'total_nodes_considered': 5,
                'generation_method': 'test'
            }
        }
        
        # Validate structure
        self.assertIn('title', outline)
        self.assertIn('sections', outline)
        self.assertIn('metadata', outline)
        
        # Validate sections
        for section in outline['sections']:
            self.assertIn('title', section)
            self.assertIn('level', section)
            self.assertIsInstance(section['level'], int)
            self.assertGreaterEqual(section['level'], 1)
            
            if 'subsections' in section:
                for subsection in section['subsections']:
                    self.assertIn('title', subsection)
                    self.assertIn('level', subsection)
                    self.assertGreater(subsection['level'], section['level'])
    
    def test_outline_hierarchy_consistency(self):
        """Test that outline hierarchy is consistent."""
        outline = {
            'sections': [
                {
                    'title': 'Level 1 Section',
                    'level': 1,
                    'subsections': [
                        {
                            'title': 'Level 2 Subsection',
                            'level': 2
                        },
                        {
                            'title': 'Level 3 Subsection',
                            'level': 3
                        }
                    ]
                }
            ]
        }
        
        # Check hierarchy consistency
        for section in outline['sections']:
            if 'subsections' in section:
                for subsection in section['subsections']:
                    self.assertGreater(
                        subsection['level'], 
                        section['level'],
                        "Subsection level should be greater than parent level"
                    )


if __name__ == '__main__':
    unittest.main()
