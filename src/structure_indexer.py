"""
Structure indexer module for document outline learning.
CLI tool for indexing document structures using FAISS and OpenAI embeddings.
"""

import os
import json
import argparse
import numpy as np
from typing import List, Dict, Optional
import faiss
from openai import OpenAI
from dotenv import load_dotenv

from structure_extractor import StructureExtractor, Node

# Load environment variables
load_dotenv()


class StructureIndexer:
    """Indexes document structures using FAISS and OpenAI embeddings."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the structure indexer.
        
        Args:
            openai_api_key: OpenAI API key (if not provided, uses env var)
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dim = 1536  # Dimension for text-embedding-3-small
        
        self.extractor = StructureExtractor()
        self.index = None
        self.metadata = []
    
    def index_directory(self, input_dir: str, output_path: str) -> bool:
        """
        Index all supported documents in a directory.
        
        Args:
            input_dir: Directory containing documents to index
            output_path: Path to save the FAISS index (without extension)
            
        Returns:
            True if indexing successful, False otherwise
        """
        if not os.path.exists(input_dir):
            print(f"Error: Input directory '{input_dir}' does not exist.")
            return False
        
        print(f"Indexing documents in: {input_dir}")
        
        # Collect all nodes from documents
        all_nodes = []
        supported_extensions = {'.docx', '.pdf'}
        
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in supported_extensions:
                    print(f"Processing: {file}")
                    try:
                        nodes = self.extractor.extract(file_path)
                        all_nodes.extend(nodes)
                        print(f"  Extracted {len(nodes)} structure nodes")
                    except Exception as e:
                        print(f"  Error processing {file}: {str(e)}")
        
        if not all_nodes:
            print("No structure nodes found in the directory.")
            return False
        
        print(f"Total nodes extracted: {len(all_nodes)}")
        
        # Create embeddings and build index
        return self._build_index(all_nodes, output_path)
    
    def _build_index(self, nodes: List[Node], output_path: str) -> bool:
        """
        Build FAISS index from nodes.
        
        Args:
            nodes: List of Node objects to index
            output_path: Path to save the index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print("Creating embeddings...")
            
            # Prepare texts for embedding (combine title and text_span)
            texts = []
            for node in nodes:
                # Combine title and text span for richer context
                combined_text = f"{node.title}\n{node.text_span}"
                texts.append(combined_text)
            
            # Create embeddings in batches
            embeddings = self._create_embeddings_batch(texts)
            
            if not embeddings:
                print("Failed to create embeddings.")
                return False
            
            print(f"Created {len(embeddings)} embeddings")
            
            # Build FAISS index
            print("Building FAISS index...")
            embeddings_array = np.array(embeddings).astype('float32')
            
            # Use IndexFlatL2 for exact similarity search
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.index.add(embeddings_array)
            
            # Prepare metadata
            self.metadata = []
            for i, node in enumerate(nodes):
                metadata_entry = {
                    'id': node.id,
                    'level': node.level,
                    'title': node.title,
                    'text_span': node.text_span,
                    'doc_id': node.doc_id,
                    'vector_id': i
                }
                self.metadata.append(metadata_entry)
            
            # Save index and metadata
            self._save_index(output_path)
            
            print(f"Index built successfully with {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            print(f"Error building index: {str(e)}")
            return False
    
    def _create_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Create embeddings for texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch
            
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                print(f"  Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
                
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )
                
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)
                
            except Exception as e:
                print(f"Error creating embeddings for batch {i//batch_size + 1}: {str(e)}")
                return []
        
        return all_embeddings
    
    def _save_index(self, output_path: str) -> None:
        """
        Save FAISS index and metadata to files.
        
        Args:
            output_path: Base path for saving files (without extension)
        """
        # Save FAISS index
        faiss_path = f"{output_path}.faiss"
        faiss.write_index(self.index, faiss_path)
        print(f"FAISS index saved to: {faiss_path}")
        
        # Save metadata
        metadata_path = f"{output_path}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"Metadata saved to: {metadata_path}")
    
    def load_index(self, index_path: str) -> bool:
        """
        Load existing FAISS index and metadata.
        
        Args:
            index_path: Path to the FAISS index file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load FAISS index
            if not os.path.exists(index_path):
                print(f"Index file not found: {index_path}")
                return False
            
            self.index = faiss.read_index(index_path)
            
            # Load metadata
            base_path = index_path.replace('.faiss', '')
            metadata_path = f"{base_path}_metadata.json"
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            else:
                print(f"Warning: Metadata file not found: {metadata_path}")
                self.metadata = []
            
            print(f"Index loaded successfully with {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            print(f"Error loading index: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar structure nodes.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of search results with metadata
        """
        if not self.index:
            raise ValueError("Index not loaded. Call load_index() first.")
        
        try:
            # Create embedding for query
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=[query]
            )
            query_embedding = np.array([response.data[0].embedding]).astype('float32')
            
            # Search in FAISS index
            distances, indices = self.index.search(query_embedding, top_k)
            
            # Prepare results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.metadata):
                    result = self.metadata[idx].copy()
                    result['similarity_score'] = float(1 / (1 + distance))  # Convert distance to similarity
                    result['rank'] = i + 1
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error during search: {str(e)}")
            return []


def main():
    """CLI entry point for structure indexer."""
    parser = argparse.ArgumentParser(description="Index document structures using FAISS and OpenAI embeddings")
    parser.add_argument("--in_dir", required=True, help="Input directory containing documents")
    parser.add_argument("--out", required=True, help="Output path for index (without extension)")
    parser.add_argument("--api_key", help="OpenAI API key (optional, uses env var if not provided)")
    
    args = parser.parse_args()
    
    try:
        indexer = StructureIndexer(openai_api_key=args.api_key)
        success = indexer.index_directory(args.in_dir, args.out)
        
        if success:
            print("Indexing completed successfully!")
            return 0
        else:
            print("Indexing failed.")
            return 1
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
