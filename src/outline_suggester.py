"""
Outline suggester module for document outline learning.
CLI tool for suggesting hierarchical outlines based on requirements and indexed structures.
"""

import os
import json
import argparse
from typing import List, Dict, Set
from collections import Counter, defaultdict
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

from structure_indexer import StructureIndexer
from structure_extractor import StructureExtractor

# Load environment variables
load_dotenv()


class OutlineSuggester:
    """Suggests hierarchical outlines based on requirements and indexed structures."""
    
    def __init__(self, faiss_index_path: str, metadata_path: str, openai_api_key: str = None):
        """
        Initialize the outline suggester.
        
        Args:
            faiss_index_path: Path to FAISS index file
            metadata_path: Path to metadata JSON file
            openai_api_key: OpenAI API key (optional, uses env var if not provided)
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Initialize indexer and load index
        self.indexer = StructureIndexer(self.api_key)
        if not self.indexer.load_index(faiss_index_path):
            raise ValueError(f"Failed to load FAISS index from {faiss_index_path}")
        
        # Load metadata separately if provided
        if metadata_path and os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = self.indexer.metadata
        
        self.extractor = StructureExtractor()
    
    def suggest_outline(self, requirements_path: str, top_k: int = 5) -> Dict:
        """
        Suggest hierarchical outline based on requirements document.
        
        Args:
            requirements_path: Path to requirements document (PDF or DOCX)
            top_k: Number of top similar headings to consider
            
        Returns:
            Dictionary containing hierarchical outline structure
        """
        print(f"Processing requirements from: {requirements_path}")
        
        # Extract requirements text
        requirements_text = self._extract_requirements_text(requirements_path)
        if not requirements_text:
            raise ValueError("Could not extract text from requirements document")
        
        print(f"Extracted {len(requirements_text)} characters from requirements")
        
        # Search for similar heading nodes
        print(f"Searching for top {top_k} similar headings...")
        similar_nodes = self.indexer.search(requirements_text, top_k * 3)  # Get more for filtering
        
        if not similar_nodes:
            print("No similar nodes found, using default outline")
            return self._get_default_outline()
        
        print(f"Found {len(similar_nodes)} similar nodes")
        
        # Apply frequency and semantic deduplication
        deduplicated_nodes = self._deduplicate_nodes(similar_nodes, top_k)
        
        # Generate hierarchical outline
        outline = self._generate_hierarchical_outline(deduplicated_nodes, requirements_text)
        
        return outline
    
    def _extract_requirements_text(self, requirements_path: str) -> str:
        """Extract text from requirements document."""
        try:
            nodes = self.extractor.extract(requirements_path)
            
            # Combine all text from nodes
            text_parts = []
            for node in nodes:
                text_parts.append(f"{node.title}\n{node.text_span}")
            
            return '\n\n'.join(text_parts)
            
        except Exception as e:
            print(f"Error extracting requirements text: {str(e)}")
            return ""
    
    def _deduplicate_nodes(self, nodes: List[Dict], target_count: int) -> List[Dict]:
        """
        Apply frequency and semantic deduplication to nodes.
        
        Args:
            nodes: List of similar nodes from search
            target_count: Target number of nodes to return
            
        Returns:
            Deduplicated list of nodes
        """
        if not nodes:
            return []
        
        # Group by similarity and frequency
        title_groups = defaultdict(list)
        
        for node in nodes:
            # Normalize title for grouping
            normalized_title = self._normalize_title(node['title'])
            title_groups[normalized_title].append(node)
        
        # Select best representative from each group
        deduplicated = []
        for group_title, group_nodes in title_groups.items():
            # Sort by similarity score and take the best one
            best_node = max(group_nodes, key=lambda x: x.get('similarity_score', 0))
            
            # Add frequency information
            best_node['frequency'] = len(group_nodes)
            deduplicated.append(best_node)
        
        # Sort by combination of similarity and frequency
        deduplicated.sort(key=lambda x: (x.get('similarity_score', 0) * 0.7 + 
                                       min(x.get('frequency', 1) / 10, 0.3)), reverse=True)
        
        return deduplicated[:target_count]
    
    def _normalize_title(self, title: str) -> str:
        """Normalize title for grouping similar headings."""
        import re
        
        # Remove numbers, punctuation, and normalize case
        normalized = re.sub(r'^\d+\.?\s*', '', title)  # Remove leading numbers
        normalized = re.sub(r'[^\w\s]', '', normalized)  # Remove punctuation
        normalized = normalized.lower().strip()
        
        # Handle common variations
        replacements = {
            'executive summary': 'executive_summary',
            'project information': 'project_info',
            'project goals': 'goals',
            'objectives': 'goals',
            'responsibilities': 'roles',
            'deliverables': 'deliverables',
            'timeline': 'schedule',
            'implementation': 'implementation'
        }
        
        for old, new in replacements.items():
            if old in normalized:
                normalized = new
                break
        
        return normalized
    
    def _generate_hierarchical_outline(self, nodes: List[Dict], requirements_text: str) -> Dict:
        """
        Generate hierarchical outline structure from deduplicated nodes.
        
        Args:
            nodes: Deduplicated nodes
            requirements_text: Original requirements text
            
        Returns:
            Hierarchical outline dictionary
        """
        # Group nodes by level
        level_groups = defaultdict(list)
        for node in nodes:
            level_groups[node['level']].append(node)
        
        # Build hierarchical structure
        outline = {
            'title': 'Suggested Project Outline',
            'sections': [],
            'metadata': {
                'source_documents': list(set(node['doc_id'] for node in nodes)),
                'total_nodes_considered': len(nodes),
                'generation_method': 'frequency_semantic_dedup'
            }
        }
        
        # Start with level 1 headings
        level_1_nodes = level_groups.get(1, [])
        
        for node in level_1_nodes:
            section = {
                'title': self._clean_title(node['title']),
                'level': 1,
                'source_similarity': node.get('similarity_score', 0),
                'frequency': node.get('frequency', 1),
                'subsections': []
            }
            
            # Find related subsections (level 2+)
            section['subsections'] = self._find_subsections(node, level_groups, nodes)
            
            outline['sections'].append(section)
        
        # Add any high-level sections that might be missing
        outline = self._enhance_outline_with_requirements(outline, requirements_text)
        
        return outline
    
    def _find_subsections(self, parent_node: Dict, level_groups: Dict, all_nodes: List[Dict]) -> List[Dict]:
        """Find subsections related to a parent node."""
        subsections = []
        
        # Look for level 2 and 3 nodes that might be related
        for level in [2, 3]:
            level_nodes = level_groups.get(level, [])
            
            for node in level_nodes:
                # Simple heuristic: if from same document or similar context
                if (node['doc_id'] == parent_node['doc_id'] or 
                    self._are_related_sections(parent_node, node)):
                    
                    subsection = {
                        'title': self._clean_title(node['title']),
                        'level': level,
                        'source_similarity': node.get('similarity_score', 0),
                        'frequency': node.get('frequency', 1)
                    }
                    subsections.append(subsection)
        
        # Sort by similarity and limit
        subsections.sort(key=lambda x: x['source_similarity'], reverse=True)
        return subsections[:3]  # Limit subsections
    
    def _are_related_sections(self, parent: Dict, child: Dict) -> bool:
        """Check if two sections are semantically related."""
        # Simple keyword-based relationship check
        parent_words = set(parent['title'].lower().split())
        child_words = set(child['title'].lower().split())
        
        # Check for common words (excluding common stop words)
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        parent_words -= stop_words
        child_words -= stop_words
        
        if parent_words & child_words:  # Common words found
            return True
        
        # Check for semantic relationships (simplified)
        relationships = {
            'project': ['goals', 'objectives', 'scope', 'requirements'],
            'implementation': ['timeline', 'schedule', 'phases', 'steps'],
            'management': ['roles', 'responsibilities', 'team', 'organization'],
            'quality': ['assurance', 'control', 'testing', 'validation']
        }
        
        for parent_word in parent_words:
            if parent_word in relationships:
                related_words = relationships[parent_word]
                if any(word in child_words for word in related_words):
                    return True
        
        return False
    
    def _clean_title(self, title: str) -> str:
        """Clean and format section title."""
        import re
        
        # Remove leading numbers and clean up
        cleaned = re.sub(r'^\d+\.?\s*', '', title)
        cleaned = cleaned.strip()
        
        # Capitalize properly
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]
        
        return cleaned
    
    def _enhance_outline_with_requirements(self, outline: Dict, requirements_text: str) -> Dict:
        """Enhance outline based on specific requirements."""
        # This is a placeholder for more sophisticated requirement analysis
        # Could use NLP to extract key requirements and ensure they're covered
        
        # Add a requirements analysis section if not present
        has_requirements_section = any(
            'requirement' in section['title'].lower() 
            for section in outline['sections']
        )
        
        if not has_requirements_section and 'requirement' in requirements_text.lower():
            requirements_section = {
                'title': 'Requirements Analysis',
                'level': 1,
                'source_similarity': 0.8,
                'frequency': 1,
                'subsections': []
            }
            outline['sections'].insert(1, requirements_section)  # Insert near beginning
        
        return outline
    
    def _get_default_outline(self) -> Dict:
        """Return a default outline structure."""
        return {
            'title': 'Default Project Outline',
            'sections': [
                {'title': 'Executive Summary', 'level': 1, 'subsections': []},
                {'title': 'Project Information', 'level': 1, 'subsections': []},
                {'title': 'Project Goals and Objectives', 'level': 1, 'subsections': []},
                {'title': 'Implementation Plan', 'level': 1, 'subsections': []},
                {'title': 'Deliverables', 'level': 1, 'subsections': []},
                {'title': 'Timeline', 'level': 1, 'subsections': []}
            ],
            'metadata': {
                'source_documents': [],
                'total_nodes_considered': 0,
                'generation_method': 'default'
            }
        }


def main():
    """CLI entry point for outline suggester."""
    parser = argparse.ArgumentParser(description="Suggest hierarchical outlines based on requirements")
    parser.add_argument("--faiss", required=True, help="Path to FAISS index file")
    parser.add_argument("--metadata", help="Path to metadata JSON file (optional)")
    parser.add_argument("--requirements", required=True, help="Path to requirements document")
    parser.add_argument("--top_k", type=int, default=5, help="Number of top similar headings to consider")
    parser.add_argument("--out", required=True, help="Output path for draft outline JSON")
    parser.add_argument("--api_key", help="OpenAI API key (optional, uses env var if not provided)")
    
    args = parser.parse_args()
    
    try:
        # Use metadata path if provided, otherwise derive from faiss path
        metadata_path = args.metadata
        if not metadata_path:
            metadata_path = args.faiss.replace('.faiss', '_metadata.json')
        
        suggester = OutlineSuggester(args.faiss, metadata_path, args.api_key)
        outline = suggester.suggest_outline(args.requirements, args.top_k)
        
        # Save outline to file
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(outline, f, indent=2, ensure_ascii=False)
        
        print(f"Draft outline saved to: {args.out}")
        print(f"Generated outline with {len(outline['sections'])} main sections")
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
