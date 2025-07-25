"""
Outline and content generation module for BEP Agent.
Handles GPT-based outline and section generation.
"""

import re
from typing import List, Dict, Tuple
from openai import OpenAI
from config import Config

class OutlineGenerator:
    """Generates BEP outlines and section content using GPT."""
    
    def __init__(self):
        """Initialize the outline generator with OpenAI client."""
        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            self.openai_client = None
    
    def extract_canonical_outline(self, documents: List[Dict], selected_plans: List[str] = None) -> List[str]:
        """
        Extract a canonical outline from selected BEP documents.
        
        Args:
            documents: List of document dictionaries
            selected_plans: List of selected plan filenames (if None, use all)
            
        Returns:
            List of canonical headings
        """
        all_headings = []
        
        # Filter documents if specific plans are selected
        if selected_plans:
            documents = [doc for doc in documents if doc['filename'] in selected_plans]
        
        # Collect all headings
        for doc in documents:
            all_headings.extend(doc['headings'])
        
        # Normalize and deduplicate headings
        canonical_headings = self._normalize_headings(all_headings)
        
        return canonical_headings
    
    def _normalize_headings(self, headings: List[str]) -> List[str]:
        """
        Normalize and deduplicate headings to create a canonical structure.
        
        Args:
            headings: List of raw headings
            
        Returns:
            List of normalized canonical headings
        """
        normalized = []
        seen = set()
        
        for heading in headings:
            # Clean up the heading
            clean_heading = re.sub(r'^\d+\.?\s*', '', heading)  # Remove numbering
            clean_heading = clean_heading.strip().title()
            
            # Skip very short or very long headings
            if len(clean_heading) < 3 or len(clean_heading) > 100:
                continue
            
            # Skip duplicates (case-insensitive)
            if clean_heading.lower() not in seen:
                normalized.append(clean_heading)
                seen.add(clean_heading.lower())
        
        return normalized
    
    def generate_project_outline(self, project_description: str, context_chunks: List[Dict], 
                                canonical_headings: List[str]) -> List[str]:
        """
        Generate a tailored outline for the new project using GPT.
        
        Args:
            project_description: Description of the new project
            context_chunks: Relevant chunks from similar BEPs
            canonical_headings: Canonical headings from existing plans
            
        Returns:
            List of outline headings for the new project
        """
        # Prepare context from chunks
        context_text = self._prepare_context_text(context_chunks)
        
        # Prepare canonical headings text
        headings_text = "\n".join([f"- {heading}" for heading in canonical_headings[:20]])
        
        # Create prompt for outline generation
        prompt = f"""You are an expert BIM (Building Information Modeling) consultant creating a BIM Execution Plan (BEP) outline.

PROJECT DESCRIPTION:
{project_description}

REFERENCE HEADINGS FROM EXISTING BEPS:
{headings_text}

RELEVANT CONTEXT FROM SIMILAR PROJECTS:
{context_text}

Based on the project description and reference materials above, create a comprehensive outline for a BIM Execution Plan. 

Requirements:
1. Include all essential BEP sections appropriate for this project type
2. Adapt the structure to the specific project requirements
3. Use clear, professional heading names
4. Organize in logical order from project overview to implementation details
5. Include 8-15 main sections

Return only the outline headings, one per line, without numbering or bullets:"""

        if not self.openai_client:
            print("OpenAI client not available, using default outline")
            return self._get_default_outline()

        try:
            response = self.openai_client.chat.completions.create(
                model=Config.GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )

            outline_text = response.choices[0].message.content.strip()

            # Parse the outline into a list
            outline_headings = [line.strip() for line in outline_text.split('\n')
                              if line.strip() and not line.strip().startswith('-')]

            return outline_headings

        except Exception as e:
            print(f"Error generating outline: {str(e)}")
            # Return a default outline if GPT fails
            return self._get_default_outline()
    
    def generate_section_content(self, section_heading: str, project_description: str, 
                                context_chunks: List[Dict]) -> str:
        """
        Generate content for a specific section of the BEP.
        
        Args:
            section_heading: The heading of the section to generate
            project_description: Description of the new project
            context_chunks: Relevant chunks from similar BEPs
            
        Returns:
            Generated section content
        """
        # Prepare context from chunks
        context_text = self._prepare_context_text(context_chunks, max_chunks=3)
        
        # Create prompt for section content generation
        prompt = f"""You are an expert BIM consultant writing a section of a BIM Execution Plan (BEP).

PROJECT DESCRIPTION:
{project_description}

SECTION TO WRITE: {section_heading}

REFERENCE CONTENT FROM SIMILAR PROJECTS:
{context_text}

Write a comprehensive section for "{section_heading}" that is specifically tailored to this project. 

Requirements:
1. Write 2-4 paragraphs of professional, detailed content
2. Include specific considerations relevant to this project type
3. Reference industry standards and best practices where appropriate
4. Use clear, professional language suitable for a BEP document
5. Include actionable information and specific requirements
6. Do not include sub-headings or bullet points in the content

Write the section content:"""

        if not self.openai_client:
            return f"Content for {section_heading} section would be generated here based on project requirements and industry best practices. (OpenAI API not available)"

        try:
            response = self.openai_client.chat.completions.create(
                model=Config.GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating section content for '{section_heading}': {str(e)}")
            return f"Content for {section_heading} section would be generated here based on project requirements and industry best practices."
    
    def generate_complete_bep(self, project_description: str, outline: List[str], 
                             context_chunks: List[Dict]) -> Dict[str, str]:
        """
        Generate complete BEP content for all sections.
        
        Args:
            project_description: Description of the new project
            outline: List of section headings
            context_chunks: Relevant chunks from similar BEPs
            
        Returns:
            Dictionary mapping section headings to content
        """
        bep_content = {}
        
        print(f"Generating content for {len(outline)} sections...")
        
        for i, section_heading in enumerate(outline):
            print(f"Generating section {i+1}/{len(outline)}: {section_heading}")
            
            # Get relevant chunks for this specific section
            section_chunks = self._get_section_relevant_chunks(
                section_heading, context_chunks
            )
            
            # Generate content for this section
            content = self.generate_section_content(
                section_heading, project_description, section_chunks
            )
            
            bep_content[section_heading] = content
        
        return bep_content
    
    def _prepare_context_text(self, chunks: List[Dict], max_chunks: int = 5) -> str:
        """
        Prepare context text from chunks for GPT prompts.
        
        Args:
            chunks: List of chunk dictionaries
            max_chunks: Maximum number of chunks to include
            
        Returns:
            Formatted context text
        """
        if not chunks:
            return "No relevant context available."
        
        context_parts = []
        for i, chunk in enumerate(chunks[:max_chunks]):
            source = chunk.get('source_file', 'Unknown')
            heading = chunk.get('relevant_heading', 'General')
            text = chunk.get('text', '')
            
            context_parts.append(f"[Source: {source} - {heading}]\n{text}\n")
        
        return "\n".join(context_parts)
    
    def _get_section_relevant_chunks(self, section_heading: str, 
                                   all_chunks: List[Dict]) -> List[Dict]:
        """
        Get chunks most relevant to a specific section.
        
        Args:
            section_heading: The section heading
            all_chunks: All available chunks
            
        Returns:
            List of most relevant chunks for the section
        """
        # Simple keyword matching for section relevance
        section_keywords = section_heading.lower().split()
        
        scored_chunks = []
        for chunk in all_chunks:
            score = 0
            chunk_text = chunk.get('text', '').lower()
            chunk_heading = chunk.get('relevant_heading', '').lower()
            
            # Score based on keyword matches
            for keyword in section_keywords:
                if keyword in chunk_text:
                    score += 1
                if keyword in chunk_heading:
                    score += 2
            
            if score > 0:
                chunk_copy = chunk.copy()
                chunk_copy['section_relevance_score'] = score
                scored_chunks.append(chunk_copy)
        
        # Sort by relevance and return top chunks
        scored_chunks.sort(key=lambda x: x['section_relevance_score'], reverse=True)
        return scored_chunks[:3]
    
    def _get_default_outline(self) -> List[str]:
        """
        Return a default BEP outline if GPT generation fails.
        
        Returns:
            List of default section headings
        """
        return [
            "Executive Summary",
            "Project Information",
            "Project Goals and BIM Objectives",
            "Organizational Roles and Responsibilities",
            "BIM Process Design",
            "BIM Information Exchanges",
            "BIM Deliverables",
            "Technology Infrastructure",
            "Model Quality Assurance",
            "Collaboration Procedures",
            "Model Management and File Naming",
            "Implementation Timeline",
            "Training Requirements",
            "Appendices"
        ]
