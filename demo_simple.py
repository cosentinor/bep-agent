"""
Simple demo script for BEP Agent that works without external dependencies.
This demonstrates the core functionality without requiring OpenAI API or sentence-transformers.
"""

import os
import sys
from document_loader import DocumentLoader
from config import Config

def simple_demo():
    """Run a simple demonstration of the BEP Agent functionality."""
    
    print("🏗️ BEP Agent - Simple Demo")
    print("=" * 50)
    
    # Initialize document loader
    print("\n1. Initializing Document Loader...")
    try:
        loader = DocumentLoader()
        print("✅ Document loader initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing document loader: {e}")
        return False
    
    # Load BEP documents
    print("\n2. Loading BEP Documents...")
    try:
        documents = loader.load_bep_documents()
        if documents:
            print(f"✅ Loaded {len(documents)} BEP documents:")
            for doc in documents:
                print(f"   - {doc['filename']} ({doc['word_count']} words, {len(doc['headings'])} headings)")
        else:
            print("⚠️  No BEP documents found")
            return False
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return False
    
    # Create text chunks
    print("\n3. Creating Text Chunks...")
    try:
        chunks = loader.create_text_chunks(documents)
        print(f"✅ Created {len(chunks)} text chunks")
        
        # Show sample chunk
        if chunks:
            sample_chunk = chunks[0]
            print(f"   Sample chunk from {sample_chunk['source_file']}:")
            print(f"   Heading: {sample_chunk['relevant_heading']}")
            print(f"   Text preview: {sample_chunk['text'][:100]}...")
    except Exception as e:
        print(f"❌ Error creating chunks: {e}")
        return False
    
    # Demonstrate simple text analysis
    print("\n4. Simple Text Analysis...")
    try:
        # Count common BEP terms
        bep_terms = [
            'bim', 'model', 'coordination', 'clash', 'detection', 
            'collaboration', 'deliverable', 'responsibility', 'process'
        ]
        
        term_counts = {}
        for term in bep_terms:
            count = 0
            for doc in documents:
                count += doc['text'].lower().count(term)
            term_counts[term] = count
        
        print("✅ Term frequency analysis:")
        for term, count in sorted(term_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"   {term}: {count} occurrences")
    except Exception as e:
        print(f"❌ Error in text analysis: {e}")
        return False
    
    # Demonstrate outline extraction
    print("\n5. Extracting Document Structure...")
    try:
        all_headings = []
        for doc in documents:
            all_headings.extend(doc['headings'])
        
        print(f"✅ Found {len(all_headings)} total headings")
        print("   Common heading patterns:")
        
        # Group similar headings
        heading_groups = {}
        for heading in all_headings:
            # Simple grouping by first word
            first_word = heading.split()[0].lower() if heading.split() else 'other'
            if first_word not in heading_groups:
                heading_groups[first_word] = []
            heading_groups[first_word].append(heading)
        
        for group, headings in list(heading_groups.items())[:5]:  # Show top 5 groups
            print(f"   {group}: {len(headings)} headings")
            if headings:
                print(f"      Example: {headings[0]}")
    except Exception as e:
        print(f"❌ Error extracting structure: {e}")
        return False
    
    # Simulate project analysis
    print("\n6. Simulating Project Analysis...")
    try:
        sample_project = "New office building with 10 floors, requiring BIM coordination for MEP systems"
        print(f"   Project: {sample_project}")
        
        # Simple keyword matching for similarity
        project_keywords = sample_project.lower().split()
        doc_scores = []
        
        for doc in documents:
            score = 0
            doc_text = doc['text'].lower()
            for keyword in project_keywords:
                if keyword in doc_text:
                    score += doc_text.count(keyword)
            doc_scores.append((doc['filename'], score))
        
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        print("✅ Document similarity scores (simple keyword matching):")
        for filename, score in doc_scores:
            print(f"   {filename}: {score} matches")
    except Exception as e:
        print(f"❌ Error in project analysis: {e}")
        return False
    
    # Generate simple outline
    print("\n7. Generating Simple Outline...")
    try:
        # Extract common outline structure
        common_sections = [
            "Executive Summary",
            "Project Information", 
            "BIM Objectives",
            "Roles and Responsibilities",
            "Technology Requirements",
            "Deliverables",
            "Quality Assurance",
            "Implementation Timeline"
        ]
        
        print("✅ Generated outline for new project:")
        for i, section in enumerate(common_sections, 1):
            print(f"   {i}. {section}")
    except Exception as e:
        print(f"❌ Error generating outline: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed successfully!")
    print("\nNext steps:")
    print("1. Add your OpenAI API key to .env file for AI-powered features")
    print("2. Install sentence-transformers for local embeddings")
    print("3. Run 'streamlit run main.py' for the full web interface")
    
    return True

if __name__ == "__main__":
    success = simple_demo()
    sys.exit(0 if success else 1)
