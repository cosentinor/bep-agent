"""
Document loader module for BEP Agent.
Handles loading and text extraction from DOCX files.
"""

import os
import re
from typing import List, Dict, Tuple
from docx import Document
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    # Fallback for older langchain versions
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config

class DocumentLoader:
    """Handles loading and processing of BEP documents."""
    
    def __init__(self):
        """Initialize the document loader with text splitter."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_docx(self, file_path: str) -> Tuple[str, List[str]]:
        """
        Extract text and headings from a DOCX file.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            Tuple of (full_text, headings_list)
        """
        try:
            doc = Document(file_path)
            full_text = []
            headings = []
            
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if text:
                    # Check if this is a heading based on style
                    if paragraph.style.name.startswith('Heading'):
                        headings.append(text)
                    full_text.append(text)
            
            return "\n".join(full_text), headings
            
        except Exception as e:
            print(f"Error extracting text from {file_path}: {str(e)}")
            return "", []
    
    def extract_headings_from_text(self, text: str) -> List[str]:
        """
        Extract headings from text using regex patterns.
        
        Args:
            text: The text to extract headings from
            
        Returns:
            List of extracted headings
        """
        headings = []
        
        # Pattern for numbered headings (1., 1.1, 1.1.1, etc.)
        numbered_pattern = r'^(\d+(?:\.\d+)*\.?\s+.+)$'
        
        # Pattern for capitalized headings
        caps_pattern = r'^([A-Z][A-Z\s]{3,})$'
        
        # Pattern for title case headings
        title_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):?$'
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for numbered headings
            if re.match(numbered_pattern, line, re.MULTILINE):
                headings.append(line)
            # Check for all caps headings
            elif re.match(caps_pattern, line):
                headings.append(line)
            # Check for title case headings
            elif re.match(title_pattern, line) and len(line.split()) <= 8:
                headings.append(line)
        
        return headings
    
    def load_bep_documents(self) -> List[Dict]:
        """
        Load all BEP documents from the samples directory.
        
        Returns:
            List of document dictionaries with text, headings, and metadata
        """
        documents = []
        
        if not os.path.exists(Config.BEP_SAMPLES_DIR):
            print(f"BEP samples directory not found: {Config.BEP_SAMPLES_DIR}")
            return documents
        
        for filename in os.listdir(Config.BEP_SAMPLES_DIR):
            if filename.endswith('.docx') and not filename.startswith('~'):
                file_path = os.path.join(Config.BEP_SAMPLES_DIR, filename)
                print(f"Loading document: {filename}")
                
                text, headings = self.extract_text_from_docx(file_path)
                
                if text:
                    # If no headings were extracted from styles, try regex
                    if not headings:
                        headings = self.extract_headings_from_text(text)
                    
                    documents.append({
                        'filename': filename,
                        'file_path': file_path,
                        'text': text,
                        'headings': headings,
                        'word_count': len(text.split())
                    })
                else:
                    print(f"No text extracted from {filename}")
        
        print(f"Loaded {len(documents)} BEP documents")
        return documents
    
    def create_text_chunks(self, documents: List[Dict]) -> List[Dict]:
        """
        Split documents into chunks for vector embedding.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        
        for doc in documents:
            text_chunks = self.text_splitter.split_text(doc['text'])
            
            for i, chunk_text in enumerate(text_chunks):
                # Find the most relevant heading for this chunk
                relevant_heading = self._find_relevant_heading(
                    chunk_text, doc['headings'], doc['text']
                )
                
                chunk = {
                    'text': chunk_text,
                    'source_file': doc['filename'],
                    'chunk_index': i,
                    'total_chunks': len(text_chunks),
                    'relevant_heading': relevant_heading,
                    'word_count': len(chunk_text.split())
                }
                chunks.append(chunk)
        
        print(f"Created {len(chunks)} text chunks")
        return chunks
    
    def _find_relevant_heading(self, chunk_text: str, headings: List[str], full_text: str) -> str:
        """
        Find the most relevant heading for a text chunk.
        
        Args:
            chunk_text: The text chunk
            headings: List of headings from the document
            full_text: The full document text
            
        Returns:
            The most relevant heading or empty string
        """
        if not headings:
            return ""
        
        # Find the position of the chunk in the full text
        chunk_start = full_text.find(chunk_text[:100])  # Use first 100 chars for matching
        
        if chunk_start == -1:
            return headings[0] if headings else ""
        
        # Find the last heading that appears before this chunk
        relevant_heading = ""
        for heading in headings:
            heading_pos = full_text.find(heading)
            if heading_pos != -1 and heading_pos <= chunk_start:
                relevant_heading = heading
        
        return relevant_heading
    
    def load_project_requirements(self, file_path: str = None, text_input: str = None) -> str:
        """
        Load project requirements from file or text input.
        
        Args:
            file_path: Path to requirements document
            text_input: Direct text input
            
        Returns:
            Project requirements text
        """
        if file_path and os.path.exists(file_path):
            if file_path.endswith('.docx'):
                text, _ = self.extract_text_from_docx(file_path)
                return text
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        elif text_input:
            return text_input
        else:
            return ""
