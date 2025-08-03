"""
BEP Agent Outline Learning Package

This package provides document structure extraction, indexing, and outline generation
capabilities for the BEP (BIM Execution Plan) Agent project.
"""

__version__ = "0.1.0"
__author__ = "BEP Agent Team"

# Import main classes for easy access
from .structure_extractor import StructureExtractor, Node, extract, parse_docx, parse_pdf
from .structure_indexer import StructureIndexer
from .outline_suggester import OutlineSuggester

__all__ = [
    "StructureExtractor",
    "Node", 
    "extract",
    "parse_docx",
    "parse_pdf",
    "StructureIndexer",
    "OutlineSuggester",
]
