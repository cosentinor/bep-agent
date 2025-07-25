"""
Vector store module for BEP Agent.
Handles embedding generation and FAISS similarity search.
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Tuple
import faiss
from openai import OpenAI
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

class VectorStore:
    """Manages vector embeddings and similarity search using FAISS."""
    
    def __init__(self):
        """Initialize the vector store with embedding model."""
        self.openai_client = None
        self.sentence_model = None
        self.faiss_index = None
        self.chunks_metadata = []
        self.plan_vectors = {}
        self.embedding_dim = None
        
        # Initialize embedding model based on configuration
        if Config.USE_LOCAL_EMBEDDINGS:
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                print("Initializing local sentence transformer model...")
                self.sentence_model = SentenceTransformer(Config.LOCAL_EMBEDDING_MODEL)
                self.embedding_dim = self.sentence_model.get_sentence_embedding_dimension()
            else:
                print("Warning: sentence-transformers not available, falling back to OpenAI")
                self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.embedding_dim = 1536
        else:
            print("Initializing OpenAI embedding model...")
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.embedding_dim = 1536  # Dimension for text-embedding-ada-002
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for a text string.
        
        Args:
            text: Text to embed
            
        Returns:
            Numpy array of embedding vector
        """
        try:
            if Config.USE_LOCAL_EMBEDDINGS and self.sentence_model:
                return self.sentence_model.encode([text])[0]
            else:
                response = self.openai_client.embeddings.create(
                    model=Config.EMBEDDING_MODEL,
                    input=text
                )
                return np.array(response.data[0].embedding)
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            return np.zeros(self.embedding_dim)
    
    def get_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Get embeddings for a batch of texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        
        try:
            if Config.USE_LOCAL_EMBEDDINGS and self.sentence_model:
                embeddings = self.sentence_model.encode(texts)
            else:
                # Process in batches to avoid API limits
                batch_size = 100
                for i in range(0, len(texts), batch_size):
                    batch = texts[i:i + batch_size]
                    response = self.openai_client.embeddings.create(
                        model=Config.EMBEDDING_MODEL,
                        input=batch
                    )
                    batch_embeddings = [np.array(item.embedding) for item in response.data]
                    embeddings.extend(batch_embeddings)

            return embeddings

        except Exception as e:
            print(f"Error generating batch embeddings: {str(e)}")
            return [np.zeros(self.embedding_dim) for _ in texts]
    
    def build_faiss_index(self, chunks: List[Dict]) -> None:
        """
        Build FAISS index from text chunks.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
        """
        print("Building FAISS index...")
        
        # Extract texts for embedding
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.get_embeddings_batch(texts)
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Create FAISS index
        self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        
        # Normalize vectors for cosine similarity
        faiss.normalize_L2(embeddings_array)
        
        # Add vectors to index
        self.faiss_index.add(embeddings_array)
        
        # Store metadata
        self.chunks_metadata = chunks
        
        print(f"FAISS index built with {self.faiss_index.ntotal} vectors")
    
    def compute_plan_vectors(self, documents: List[Dict]) -> None:
        """
        Compute average vectors for each BEP plan.
        
        Args:
            documents: List of document dictionaries
        """
        print("Computing plan vectors...")
        
        for doc in documents:
            # Get chunks for this document
            doc_chunks = [chunk for chunk in self.chunks_metadata 
                         if chunk['source_file'] == doc['filename']]
            
            if doc_chunks:
                # Get embeddings for all chunks of this document
                chunk_texts = [chunk['text'] for chunk in doc_chunks]
                chunk_embeddings = self.get_embeddings_batch(chunk_texts)
                
                # Compute average vector
                avg_vector = np.mean(chunk_embeddings, axis=0)
                self.plan_vectors[doc['filename']] = avg_vector
        
        print(f"Computed plan vectors for {len(self.plan_vectors)} documents")
    
    def find_similar_plans(self, query_text: str, top_k: int = None) -> List[Tuple[str, float]]:
        """
        Find most similar BEP plans to a query.
        
        Args:
            query_text: Project description or requirements
            top_k: Number of top plans to return
            
        Returns:
            List of (filename, similarity_score) tuples
        """
        if top_k is None:
            top_k = Config.TOP_K_PLANS
        
        if not self.plan_vectors:
            print("No plan vectors available")
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query_text)
        
        # Compute similarities
        similarities = []
        for filename, plan_vector in self.plan_vectors.items():
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1),
                plan_vector.reshape(1, -1)
            )[0][0]
            similarities.append((filename, float(similarity)))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def search_similar_chunks(self, query_text: str, top_k: int = None) -> List[Dict]:
        """
        Search for similar chunks using FAISS.
        
        Args:
            query_text: Query text
            top_k: Number of top chunks to return
            
        Returns:
            List of chunk dictionaries with similarity scores
        """
        if top_k is None:
            top_k = Config.TOP_K_CHUNKS
        
        if self.faiss_index is None:
            print("FAISS index not built")
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query_text)
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_vector)
        
        # Search
        scores, indices = self.faiss_index.search(query_vector, top_k)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.chunks_metadata):
                chunk = self.chunks_metadata[idx].copy()
                chunk['similarity_score'] = float(score)
                chunk['rank'] = i + 1
                results.append(chunk)
        
        return results
    
    def save_vector_store(self, filepath: str = None) -> None:
        """
        Save the vector store to disk.
        
        Args:
            filepath: Path to save the vector store
        """
        if filepath is None:
            filepath = os.path.join(Config.VECTOR_STORE_PATH, "vector_store.pkl")
        
        try:
            # Save FAISS index
            if self.faiss_index is not None:
                faiss_path = filepath.replace('.pkl', '.faiss')
                faiss.write_index(self.faiss_index, faiss_path)
            
            # Save metadata and plan vectors
            data = {
                'chunks_metadata': self.chunks_metadata,
                'plan_vectors': self.plan_vectors,
                'embedding_dim': self.embedding_dim
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            
            print(f"Vector store saved to {filepath}")
            
        except Exception as e:
            print(f"Error saving vector store: {str(e)}")
    
    def load_vector_store(self, filepath: str = None) -> bool:
        """
        Load the vector store from disk.
        
        Args:
            filepath: Path to load the vector store from
            
        Returns:
            True if successful, False otherwise
        """
        if filepath is None:
            filepath = os.path.join(Config.VECTOR_STORE_PATH, "vector_store.pkl")
        
        try:
            # Load FAISS index
            faiss_path = filepath.replace('.pkl', '.faiss')
            if os.path.exists(faiss_path):
                self.faiss_index = faiss.read_index(faiss_path)
            
            # Load metadata and plan vectors
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
                
                self.chunks_metadata = data.get('chunks_metadata', [])
                self.plan_vectors = data.get('plan_vectors', {})
                self.embedding_dim = data.get('embedding_dim', self.embedding_dim)
                
                print(f"Vector store loaded from {filepath}")
                return True
            
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
        
        return False
